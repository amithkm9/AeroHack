# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.cube import Cube
from solvers.layer_by_layer import LayerByLayerSolver
from solvers.kociemba import KociembaSolver
from solvers.beginner_method import BeginnerMethodSolver

app = Flask(__name__)
# Enable CORS with specific settings
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Store active sessions (in production, use Redis or database)
sessions = {}

@app.route('/')
def home():
    """Root endpoint"""
    return jsonify({"message": "Rubik's Cube Solver API", "status": "running"})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Rubik's Cube Solver API is running!"})

@app.route('/api/cube/new', methods=['POST', 'OPTIONS'])
def create_new_cube():
    """Create a new cube instance"""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json() or {}
    session_id = data.get('session_id', 'default')
    sessions[session_id] = Cube()
    
    return jsonify({
        "session_id": session_id,
        "state": sessions[session_id].get_state(),
        "is_solved": sessions[session_id].is_solved()
    })

@app.route('/api/cube/scramble', methods=['POST', 'OPTIONS'])
def scramble_cube():
    """Scramble the cube with random moves"""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json() or {}
    session_id = data.get('session_id', 'default')
    num_moves = data.get('num_moves', 25)
    
    if session_id not in sessions:
        sessions[session_id] = Cube()
    
    scramble_moves = sessions[session_id].scramble(num_moves)
    
    return jsonify({
        "scramble_moves": scramble_moves,
        "state": sessions[session_id].get_state(),
        "is_solved": sessions[session_id].is_solved()
    })

@app.route('/api/cube/move', methods=['POST', 'OPTIONS'])
def execute_move():
    """Execute a single move on the cube"""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json() or {}
    session_id = data.get('session_id', 'default')
    move = data.get('move')
    
    if session_id not in sessions:
        sessions[session_id] = Cube()
    
    try:
        sessions[session_id].execute_move(move)
        return jsonify({
            "success": True,
            "state": sessions[session_id].get_state(),
            "is_solved": sessions[session_id].is_solved()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/cube/solve', methods=['POST', 'OPTIONS'])
def solve_cube():
    """Solve the cube using specified method"""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json() or {}
    session_id = data.get('session_id', 'default')
    method = data.get('method', 'layer_by_layer')
    
    if session_id not in sessions:
        return jsonify({"error": "No cube found for this session"}), 404
    
    cube = sessions[session_id]
    
    # Select solver based on method
    solvers = {
        'layer_by_layer': LayerByLayerSolver,
        'kociemba': KociembaSolver,
        'beginner': BeginnerMethodSolver
    }
    
    if method not in solvers:
        return jsonify({"error": f"Unknown solving method: {method}"}), 400
    
    # Create solver instance and solve
    solver = solvers[method](cube)
    start_time = time.time()
    
    try:
        result = solver.solve()
        solve_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return jsonify({
            "success": True,
            "method": method,
            "solution": result['solution'],
            "phases": result.get('phases', {}),
            "move_count": len(result['solution']),
            "solve_time": solve_time,
            "final_state": cube.get_state(),
            "is_solved": cube.is_solved()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "method": method
        }), 500

@app.route('/api/cube/state', methods=['GET', 'OPTIONS'])
def get_cube_state():
    """Get current cube state"""
    if request.method == 'OPTIONS':
        return '', 204
        
    session_id = request.args.get('session_id', 'default')
    
    if session_id not in sessions:
        sessions[session_id] = Cube()
    
    return jsonify({
        "state": sessions[session_id].get_state(),
        "is_solved": sessions[session_id].is_solved(),
        "move_history": sessions[session_id].get_move_history()
    })

@app.route('/api/cube/reset', methods=['POST', 'OPTIONS'])
def reset_cube():
    """Reset cube to solved state"""
    if request.method == 'OPTIONS':
        return '', 204
        
    data = request.get_json() or {}
    session_id = data.get('session_id', 'default')
    
    if session_id not in sessions:
        sessions[session_id] = Cube()
    
    sessions[session_id].reset()
    
    return jsonify({
        "state": sessions[session_id].get_state(),
        "is_solved": True
    })

@app.route('/api/algorithms', methods=['GET', 'OPTIONS'])
def get_algorithms():
    """Get list of available solving algorithms"""
    if request.method == 'OPTIONS':
        return '', 204
        
    return jsonify({
        "algorithms": [
            {
                "id": "layer_by_layer",
                "name": "Layer by Layer (CFOP)",
                "description": "Advanced method using Cross, F2L, OLL, and PLL",
                "difficulty": "Advanced",
                "average_moves": "50-60"
            },
            {
                "id": "kociemba",
                "name": "Kociemba Two-Phase",
                "description": "Optimal two-phase algorithm, very efficient",
                "difficulty": "Computer",
                "average_moves": "20-30"
            },
            {
                "id": "beginner",
                "name": "Beginner Method",
                "description": "Simple layer-by-layer approach for beginners",
                "difficulty": "Easy",
                "average_moves": "100-120"
            }
        ]
    })

@app.after_request
def after_request(response):
    """Handle CORS headers"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    print("Starting Rubik's Cube Solver API...")
    print("Server running at http://localhost:5001")
    print("API endpoints available at http://localhost:5001/api/")
    app.run(debug=True, host='0.0.0.0', port=5001)