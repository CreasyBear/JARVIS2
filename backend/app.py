from flask import Flask, jsonify
from flask_cors import CORS
from flask_clerk import Clerk
import logging
from logging.handlers import RotatingFileHandler

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

# ... existing routes ...