# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import traceback
from models.cube import Cube
from solvers.simple_solver import SimpleSolver

app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app, origins=["*"], methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["Content-Type"])

sessions = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "message": "Rubik's Cube Solver API is running!",
        "version": "1.0.0"
    })

@app.route('/api/cube/new', methods=['POST'])
def create_new_cube():
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id', 'default')
        sessions[session_id] = Cube()
        
        print(f"Created new cube for session: {session_id}")
        
        return jsonify({
            "session_id": session_id,
            "state": sessions[session_id].get_state(),
            "is_solved": sessions[session_id].is_solved(),
            "message": "New cube created successfully"
        })
    except Exception as e:
        print(f"Error creating new cube: {str(e)}")
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/api/cube/scramble', methods=['POST'])
def scramble_cube():
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id', 'default')
        num_moves = data.get('num_moves', 25)
        
        if session_id not in sessions:
            sessions[session_id] = Cube()
        
        # Reset cube first to ensure clean scramble
        sessions[session_id].reset()
        scramble_moves = sessions[session_id].scramble(num_moves)
        
        print(f"Scrambled cube for session {session_id} with moves: {scramble_moves}")
        
        return jsonify({
            "scramble_moves": scramble_moves,
            "state": sessions[session_id].get_state(),
            "is_solved": sessions[session_id].is_solved(),
            "message": f"Cube scrambled with {len(scramble_moves)} moves"
        })
    except Exception as e:
        print(f"Error scrambling cube: {str(e)}")
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/api/cube/move', methods=['POST'])
def execute_move():
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id', 'default')
        move = data.get('move')
        
        if not move:
            return jsonify({"success": False, "error": "No move specified"}), 400
        
        if session_id not in sessions:
            sessions[session_id] = Cube()
        
        sessions[session_id].execute_move(move)
        
        return jsonify({
            "success": True,
            "move": move,
            "state": sessions[session_id].get_state(),
            "is_solved": sessions[session_id].is_solved(),
            "move_count": len(sessions[session_id].get_move_history())
        })
    except Exception as e:
        print(f"Error executing move {move}: {str(e)}")
        return jsonify({
            "success": False, 
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 400

@app.route('/api/cube/solve', methods=['POST'])
def solve_cube():
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id', 'default')
        
        if session_id not in sessions:
            return jsonify({"success": False, "error": "No cube found for this session"}), 404
        
        cube = sessions[session_id]
        
        # Check if already solved
        if cube.is_solved():
            return jsonify({
                "success": True,
                "solution": [],
                "algorithm": "Already Solved",
                "move_count": 0,
                "solve_time": 0,
                "final_state": cube.get_state(),
                "is_solved": True,
                "message": "Cube is already solved!"
            })
        
        print(f"Solving cube for session {session_id}")
        print(f"Current cube state: {cube.get_state()}")
        
        # Create a copy of the cube for solving
        solve_cube = cube.copy()
        
        # Use the simple solver instead of Kociemba
        solver = SimpleSolver(solve_cube)
        result = solver.solve()
        
        # Get the initial state before applying solution
        initial_state = cube.get_state()
        
        # Apply solution to original cube
        print(f"Applying solution: {result['solution']}")
        for move in result['solution']:
            cube.execute_move(move)
        
        final_state = cube.get_state()
        is_solved = cube.is_solved()
        
        print(f"Solution found: {result['solution']}")
        print(f"Move count: {result['move_count']}")
        print(f"Is solved after applying solution: {is_solved}")
        
        return jsonify({
            "success": True,
            "solution": result['solution'],
            "algorithm": result.get('algorithm', 'Simple Solver'),
            "move_count": result['move_count'],
            "solve_time": result.get('solve_time', 0),
            "initial_state": initial_state,
            "final_state": final_state,
            "is_solved": is_solved,
            "message": f"Cube solved in {result['move_count']} moves!"
        })
        
    except Exception as e:
        print(f"Error solving cube: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/cube/reset', methods=['POST'])
def reset_cube():
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id', 'default')
        
        if session_id not in sessions:
            sessions[session_id] = Cube()
        else:
            sessions[session_id].reset()
        
        print(f"Reset cube for session {session_id}")
        
        return jsonify({
            "state": sessions[session_id].get_state(),
            "is_solved": True,
            "message": "Cube reset to solved state"
        })
    except Exception as e:
        print(f"Error resetting cube: {str(e)}")
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route('/api/algorithms', methods=['GET'])
def get_algorithms():
    return jsonify({
        "algorithms": [{
            "id": "simple",
            "name": "Layer-by-Layer",
            "description": "Simple and reliable layer-by-layer solving method",
            "difficulty": "Beginner",
            "average_moves": "50-80"
        }]
    })

@app.route('/api/cube/state', methods=['GET'])
def get_cube_state():
    try:
        session_id = request.args.get('session_id', 'default')
        
        if session_id not in sessions:
            sessions[session_id] = Cube()
        
        return jsonify({
            "session_id": session_id,
            "state": sessions[session_id].get_state(),
            "is_solved": sessions[session_id].is_solved(),
            "move_count": len(sessions[session_id].get_move_history())
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🎯 Starting Rubik's Cube Solver API...")
    print("🌐 Server will run at: http://localhost:5001")
    print("🔗 Health check: http://localhost:5001/api/health")
    print("=" * 50)
    app.run(debug=True, port=5001, host='0.0.0.0')