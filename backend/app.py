# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import time
from models.cube import Cube
from solvers.kociemba import KociembaSolver

app = Flask(__name__)
CORS(app)

sessions = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Rubik's Cube Solver API is running!"})

@app.route('/api/cube/new', methods=['POST'])
def create_new_cube():
    data = request.get_json() or {}
    session_id = data.get('session_id', 'default')
    sessions[session_id] = Cube()
    
    return jsonify({
        "session_id": session_id,
        "state": sessions[session_id].get_state(),
        "is_solved": sessions[session_id].is_solved()
    })

@app.route('/api/cube/scramble', methods=['POST'])
def scramble_cube():
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

@app.route('/api/cube/move', methods=['POST'])
def execute_move():
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

@app.route('/api/cube/solve', methods=['POST'])
def solve_cube():
    data = request.get_json() or {}
    session_id = data.get('session_id', 'default')
    
    if session_id not in sessions:
        return jsonify({"error": "No cube found for this session"}), 404
    
    cube = sessions[session_id]
    solver = KociembaSolver(cube)
    
    try:
        result = solver.solve()
        
        return jsonify({
            "success": True,
            "solution": result['solution'],
            "phases": result.get('phases', {}),
            "move_count": len(result['solution']),
            "solve_time": result.get('solve_time', 0),
            "final_state": cube.get_state(),
            "is_solved": cube.is_solved()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/cube/reset', methods=['POST'])
def reset_cube():
    data = request.get_json() or {}
    session_id = data.get('session_id', 'default')
    
    if session_id not in sessions:
        sessions[session_id] = Cube()
    
    sessions[session_id].reset()
    
    return jsonify({
        "state": sessions[session_id].get_state(),
        "is_solved": True
    })

@app.route('/api/algorithms', methods=['GET'])
def get_algorithms():
    return jsonify({
        "algorithms": [{
            "id": "kociemba",
            "name": "Kociemba Two-Phase",
            "description": "Optimal algorithm that solves any cube in ≤20 moves",
            "difficulty": "Optimal",
            "average_moves": "18-20"
        }]
    })

if __name__ == '__main__':
    print("Starting Rubik's Cube Solver API...")
    print("Server running at http://localhost:5000")
    app.run(debug=True, port=5000)