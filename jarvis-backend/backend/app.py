from flask import Flask, jsonify, request  # Added 'request' import
from flask_cors import CORS
from flask_clerk import Clerk  # Ensure only necessary imports are present
import logging
from logging.handlers import RotatingFileHandler
from src.information_service import information_service  # Import InformationService
from src.multi_agent_workflow import execute_agents  # Updated import for execute_agents

app = Flask(__name__)
CORS(app)
Clerk(app, secret_key='your-clerk-secret-key')

# Set up logging
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Initialize Redis connection before the first request
@app.before_first_request
def startup():
    import asyncio
    from src.cache import init_redis
    asyncio.create_task(init_redis())

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled exception: {e}", exc_info=True)
    return jsonify(error="An unexpected error occurred. Please try again later."), 500

# Protected route example
@app.route('/api/protected', methods=['GET'])
@Clerk.auth_required
def protected_route():
    user = Clerk.current_user()
    return jsonify(message=f"Hello, {user.first_name}!")

# New API Endpoint for query handling
@app.route('/api/query', methods=['POST'])
@Clerk.auth_required
async def handle_query():
    query = request.json.get('query')
    if not query:
        return jsonify(error="Query not provided."), 400
    try:
        response = await information_service.execute(query)
        return jsonify(response=response)
    except Exception as e:
        app.logger.error(f"Query execution failed: {e}", exc_info=True)
        return jsonify(error="Failed to process the query."), 500

# New route for executing tasks
@app.route('/execute', methods=['POST'])
async def execute():
    task = request.json
    try:
        result = await execute_agents(task)
        return jsonify({'status': 'success', 'result': result})
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# ... existing routes ...

# ... additional routes and configurations ...