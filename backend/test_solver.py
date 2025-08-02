# backend/test_solver.py
"""Test script to verify the optimal solver works correctly"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.cube import Cube
from solvers.optimal_solver import OptimalSolver
import time

def test_solver():
    """Test the optimal solver with various scrambles"""
    
    print("=" * 60)
    print("🧪 Testing Optimal Rubik's Cube Solver")
    print("=" * 60)
    
    # Test cases
    test_scrambles = [
        # Easy scrambles
        ["R", "U", "R'", "U'"],
        ["F", "R", "U", "R'", "U'", "F'"],
        
        # Medium scrambles
        ["R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'", "U'", "R", "U", "R'", "F'"],
        ["U", "R", "U'", "L'", "U", "R'", "U'", "L", "U2"],
        
        # Hard scrambles
        ["R", "U", "R'", "F'", "R", "U", "R'", "U'", "R'", "F", "R2", "U'", "R'", "U'", 
         "F", "U", "R", "U'", "R'", "F'", "U2", "R", "U", "R'", "U", "R", "U2", "R'"],
        
        # Random 25-move scramble
        ["U", "R2", "F", "B", "R", "B2", "R", "U2", "L", "B2", "R", "U'", "D'", "R2", 
         "F'", "D2", "U'", "B2", "U2", "R'", "D2", "F2", "U2", "R2", "D2"]
    ]
    
    total_moves = 0
    total_time = 0
    successful_solves = 0
    
    for i, scramble in enumerate(test_scrambles, 1):
        print(f"\n🎲 Test {i}: Scramble with {len(scramble)} moves")
        print(f"Scramble: {' '.join(scramble)}")
        
        # Create and scramble cube
        cube = Cube()
        for move in scramble:
            cube.execute_move(move)
        
        print("Initial state analysis:")
        analysis = cube.analyze_state()
        print(f"  Solve percentage: {analysis['solve_percentage']:.1f}%")
        
        # Solve the cube
        solver = OptimalSolver(cube)
        start_time = time.time()
        
        try:
            result = solver.solve()
            solve_time = (time.time() - start_time) * 1000
            
            # Verify solution
            test_cube = Cube()
            for move in scramble:
                test_cube.execute_move(move)
            for move in result['solution']:
                test_cube.execute_move(move)
            
            is_solved = test_cube.is_solved()
            
            print(f"\n✅ Results:")
            print(f"  Algorithm: {result['algorithm']}")
            print(f"  Moves: {result['move_count']}")
            print(f"  Time: {solve_time:.1f}ms")
            print(f"  Solved: {'YES' if is_solved else 'NO'}")
            
            if len(result['solution']) <= 30:
                print(f"  Solution: {' '.join(result['solution'])}")
            else:
                print(f"  Solution: {' '.join(result['solution'][:15])} ... {' '.join(result['solution'][-15:])}")
            
            if is_solved:
                successful_solves += 1
                total_moves += result['move_count']
                total_time += solve_time
            
        except Exception as e:
            print(f"\n❌ Solver failed: {str(e)}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Total tests: {len(test_scrambles)}")
    print(f"Successful solves: {successful_solves}/{len(test_scrambles)}")
    
    if successful_solves > 0:
        avg_moves = total_moves / successful_solves
        avg_time = total_time / successful_solves
        print(f"Average moves: {avg_moves:.1f}")
        print(f"Average time: {avg_time:.1f}ms")
        
        if avg_moves <= 30:
            print("🏆 Excellent performance! Near-optimal solutions.")
        elif avg_moves <= 50:
            print("👍 Good performance! Efficient solutions.")
        else:
            print("⚠️ Solutions are working but could be more optimal.")
    
    print("\n✨ Test complete!")

def test_specific_case():
    """Test a specific challenging case"""
    print("\n" + "=" * 60)
    print("🎯 Testing Specific Challenging Case")
    print("=" * 60)
    
    cube = Cube()
    
    # Superflip pattern - one of the hardest positions (requires exactly 20 moves)
    superflip = ["R", "U2", "R'", "U'", "R", "U'", "R'", "U'", "R", "U", "R'", "U", 
                 "R", "U2", "R'", "U", "F", "U2", "F'", "U'", "F", "U'", "F'", "U'", 
                 "F", "U", "F'", "U", "F", "U2", "F'", "U"]
    
    print(f"Applying superflip pattern ({len(superflip)} moves)...")
    for move in superflip[:20]:  # Apply first 20 moves
        cube.execute_move(move)
    
    print("\nCube state after scramble:")
    cube.print_state()
    
    # Solve
    solver = OptimalSolver(cube)
    result = solver.solve()
    
    print(f"\nSolution found:")
    print(f"  Algorithm: {result['algorithm']}")
    print(f"  Moves: {result['move_count']}")
    print(f"  Time: {result['solve_time']:.1f}ms")
    
    # Verify
    for move in result['solution']:
        cube.execute_move(move)
    
    print(f"  Verified: {'✅ SOLVED' if cube.is_solved() else '❌ NOT SOLVED'}")

if __name__ == "__main__":
    test_solver()
    test_specific_case()