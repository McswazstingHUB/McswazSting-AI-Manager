import os
import sys
import logging
from datetime import datetime

# Set up paths BEFORE any other imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
logs_dir = os.path.join(project_root, 'logs')

# Create logs directory if it doesn't exist
os.makedirs(logs_dir, exist_ok=True)

log_file = os.path.join(logs_dir, 'api_server.log')

# Configure logging BEFORE importing Flask
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Now import Flask and other modules
from flask import Flask, request, jsonify
from flask_cors import CORS
from app import AIManagerCore

# Initialize Flask application
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["*"]}})

# Initialize AI Core
ai_core = AIManagerCore()

# API Routes

@app.route('/api/status', methods=['GET'])
def get_status():
    """Retrieve current system status and health metrics."""
    try:
        status_data = {
            "service": "McswazSting AI Manager",
            "status": "Online",
            "core_status": ai_core.system_status,
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "environment": "production"
        }
        logger.info("Status endpoint accessed successfully")
        return jsonify(status_data), 200
    except Exception as e:
        logger.error(f"Error retrieving status: {str(e)}")
        return jsonify({"error": "Failed to retrieve status"}), 500

@app.route('/api/process', methods=['POST'])
def process_task():
    """Process AI tasks with payload data from frontend."""
    try:
        payload = request.get_json()
        
        if not payload:
            logger.warning("Empty payload received")
            return jsonify({"error": "Payload required"}), 400
        
        task_data = payload.get('task', 'Default Task')
        logger.info(f"Processing task: {task_data}")
        
        result = ai_core.process_ai_task(task_data)
        
        response = {
            "task": task_data,
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        logger.info(f"Task processed successfully: {task_data}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing task: {str(e)}")
        return jsonify({"error": "Task processing failed", "details": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return jsonify({"health": "ok"}), 200

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Retrieve recent API logs (limited to last 50 lines)."""
    try:
        if not os.path.exists(log_file):
            return jsonify({"logs": []}), 200
        
        with open(log_file, 'r') as f:
            logs = f.readlines()[-50:]
        
        return jsonify({"logs": logs}), 200
    except Exception as e:
        logger.error(f"Error retrieving logs: {str(e)}")
        return jsonify({"error": "Failed to retrieve logs"}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"404 error: {request.path}")
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"500 error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logger.info("═" * 80)
    logger.info("McswazSting AI Manager - Flask API Server (Cyber Security Edition)")
    logger.info("═" * 80)
    logger.info(f"Project Root: {project_root}")
    logger.info(f"Logs Directory: {logs_dir}")
    logger.info(f"Log File: {log_file}")
    logger.info("CORS enabled for all origins on /api/* endpoints")
    logger.info("Server running on http://0.0.0.0:5000")
    logger.info("═" * 80)
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
