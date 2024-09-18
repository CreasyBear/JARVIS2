import os
from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from user_management import User, create_user, get_user
from monitoring import SystemMonitor
from task_planner_agent import TaskPlannerAgent
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from logger import setup_logger
from flask_caching import Cache
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from redis import Redis
from redis.exceptions import ConnectionError as RedisConnectionError

# Load environment variables
load_dotenv()

# Set up logging
dashboard_logger = setup_logger('dashboard', 'logs/dashboard.log')

# Initialize the app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_secret_key')
login_manager = LoginManager()
login_manager.init_app(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Initialize Redis with error handling
try:
    redis = Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=int(os.getenv('REDIS_PORT', 6379)), db=0)
    redis.ping()
    dashboard_logger.info("Successfully connected to Redis")
except RedisConnectionError:
    dashboard_logger.warning("Failed to connect to Redis. Using in-memory storage for rate limiting.")
    redis = None

# Configure Flask-Limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}" if redis else "memory://"
)

# Create necessary directories
DATA_DIR = 'data'
UPLOAD_FOLDER = 'uploads'
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the knowledge base
try:
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    task_planner = TaskPlannerAgent(index)
except Exception as e:
    dashboard_logger.error(f"Error loading knowledge base: {str(e)}")
    index = VectorStoreIndex([])
    task_planner = TaskPlannerAgent(index)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

system_monitor = SystemMonitor()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'message': 'Image uploaded successfully', 'filename': filename})
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/metrics', methods=['GET'])
@login_required
def get_metrics():
    dashboard_logger.info("Metrics endpoint called")
    try:
        metrics = system_monitor.get_system_metrics()
        dashboard_logger.info(f"Retrieved metrics: {metrics}")
        if not metrics:
            dashboard_logger.error("Metrics are empty")
            return jsonify({'error': 'No metrics available'}), 500
        if isinstance(metrics, dict) and 'error' in metrics:
            dashboard_logger.error(f"Error in metrics: {metrics['error']}")
            return jsonify({'error': metrics['error']}), 500
        return jsonify(metrics)
    except Exception as e:
        dashboard_logger.error(f"Error in get_metrics route: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = get_user(data['username'])
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'})
    return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/query', methods=['POST'])
@login_required
@limiter.limit("10 per minute")
def query():
    try:
        user_query = request.json['query']
        image_filename = request.json.get('image_filename')
        dashboard_logger.info(f"Received query: {user_query}")

        response = task_planner.process_query(user_query, image_filename)
        dashboard_logger.info(f"Query response: {response}")
        return jsonify({'response': response})
    except Exception as e:
        dashboard_logger.error(f"Error processing query: {str(e)}")
        return jsonify({'error': str(e)}), 500

@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)

csp = {
    'default-src': "'self'",
    'script-src': ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
    'style-src': ["'self'", "'unsafe-inline'"],
    'img-src': ["'self'", 'data:', 'blob:'],
    'font-src': ["'self'", 'data:'],
    'connect-src': ["'self'", 'http://localhost:5000'],
}

Talisman(app, content_security_policy=csp, force_https=False)