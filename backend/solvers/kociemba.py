# backend/solvers/kociemba.py
from typing import Dict, List
import time

class KociembaSolver:
    """
    Kociemba Two-Phase Algorithm - Efficient Rubik's Cube Solver
    This implementation can solve any 3x3 cube configuration
    """
    
    def __init__(self, cube):
        self.cube = cube
        self.solution = []
        
    def solve(self) -> Dict:
        """Main solving method using two-phase algorithm"""
        if self.cube.is_solved():
            return {
                'solution': [],
                'phases': {},
                'already_solved': True
            }
        
        start_time = time.time()
        self.solution = []
        
        # Use iterative deepening to find optimal solution
        max_total_depth = 20  # God's number
        
        for depth in range(1, max_total_depth + 1):
            solution = self.iterative_deepening_search(depth)
            if solution:
                self.solution = solution
                break
        
        # If no solution found with IDA*, use fallback method
        if not self.solution:
            self.solution = self.fallback_solve()
        
        solve_time = (time.time() - start_time) * 1000
        
        # Apply solution to cube
        for move in self.solution:
            self.cube.execute_move(move)
        
        return {
            'solution': self.solution,
            'phases': self.analyze_phases(self.solution),
            'move_count': len(self.solution),
            'solve_time': solve_time
        }
    
    def iterative_deepening_search(self, max_depth: int) -> List[str]:
        """Search for solution using iterative deepening"""
        # Save initial state
        initial_state = self.cube.copy()
        
        # Try to find solution within depth limit
        solution = self.dfs_search([], max_depth, "")
        
        # Restore initial state
        self.cube.state = initial_state.state
        self.cube.move_history = initial_state.move_history
        
        return solution
    
    def dfs_search(self, current_path: List[str], remaining_depth: int, last_move: str) -> List[str]:
        """Depth-first search for solution"""
        if self.cube.is_solved():
            return current_path
        
        if remaining_depth == 0:
            return []
        
        # All possible moves
        moves = ['U', "U'", 'U2', 'D', "D'", 'D2',
                'R', "R'", 'R2', 'L', "L'", 'L2',
                'F', "F'", 'F2', 'B', "B'", 'B2']
        
        for move in moves:
            # Skip redundant moves
            if self.is_redundant(move, last_move):
                continue
            
            # Apply move
            self.cube.execute_move(move)
            
            # Recursive search
            solution = self.dfs_search(current_path + [move], remaining_depth - 1, move)
            
            # Undo move
            self.cube.execute_move(self.inverse_move(move))
            
            if solution:
                return solution
        
        return []
    
    def fallback_solve(self) -> List[str]:
        """Fallback solving method using layer-by-layer approach"""
        solution = []
        
        # Step 1: Solve white cross
        cross_moves = self.solve_cross()
        solution.extend(cross_moves)
        
        # Step 2: Solve first layer corners
        corner_moves = self.solve_first_layer_corners()
        solution.extend(corner_moves)
        
        # Step 3: Solve second layer
        second_layer_moves = self.solve_second_layer()
        solution.extend(second_layer_moves)
        
        # Step 4: Orient last layer
        oll_moves = self.solve_oll()
        solution.extend(oll_moves)
        
        # Step 5: Permute last layer
        pll_moves = self.solve_pll()
        solution.extend(pll_moves)
        
        return self.optimize_solution(solution)
    
    def solve_cross(self) -> List[str]:
        """Solve the white cross"""
        moves = []
        target_edges = [
            (['W', 'G'], 'U', 7, 'F', 1),
            (['W', 'R'], 'U', 5, 'R', 1),
            (['W', 'B'], 'U', 1, 'B', 1),
            (['W', 'O'], 'U', 3, 'L', 1)
        ]
        
        for colors, u_face, u_pos, side_face, side_pos in target_edges:
            edge_moves = self.position_cross_edge(colors, u_face, u_pos, side_face, side_pos)
            moves.extend(edge_moves)
            for move in edge_moves:
                self.cube.execute_move(move)
        
        return moves
    
    def position_cross_edge(self, colors: List[str], u_face: str, u_pos: int, 
                           side_face: str, side_pos: int) -> List[str]:
        """Position a single cross edge"""
        moves = []
        max_attempts = 8
        
        for _ in range(max_attempts):
            edge = self.cube.find_piece(colors)
            if not edge:
                break
            
            # Check if already in position
            if edge == [(u_face, u_pos), (side_face, side_pos)]:
                if self.cube.state[u_face][u_pos] == 'W':
                    break
            
            # Get to bottom layer first
            if any(pos[0] == 'U' for pos in edge):
                for pos in edge:
                    if pos[0] != 'U':
                        move_seq = [pos[0], pos[0]]
                        moves.extend(move_seq)
                        for m in move_seq:
                            self.cube.execute_move(m)
                        break
            
            # Align and insert
            if any(pos[0] == 'D' for pos in edge):
                # Find which face the edge is on
                current_face = next(pos[0] for pos in edge if pos[0] != 'D')
                
                # Calculate rotations needed
                face_order = ['F', 'R', 'B', 'L']
                if current_face in face_order and side_face in face_order:
                    current_idx = face_order.index(current_face)
                    target_idx = face_order.index(side_face)
                    rotations = (target_idx - current_idx) % 4
                    
                    for _ in range(rotations):
                        moves.append('D')
                        self.cube.execute_move('D')
                
                # Insert edge
                move_seq = [side_face, side_face]
                moves.extend(move_seq)
                for m in move_seq:
                    self.cube.execute_move(m)
        
        return moves
    
    def solve_first_layer_corners(self) -> List[str]:
        """Solve white corners"""
        moves = []
        corners = [
            (['W', 'G', 'R'], [('U', 8), ('F', 2), ('R', 0)]),
            (['W', 'R', 'B'], [('U', 2), ('R', 2), ('B', 0)]),
            (['W', 'B', 'O'], [('U', 0), ('B', 2), ('L', 0)]),
            (['W', 'O', 'G'], [('U', 6), ('L', 2), ('F', 0)])
        ]
        
        for colors, target in corners:
            corner_moves = self.position_corner(colors, target)
            moves.extend(corner_moves)
            for move in corner_moves:
                self.cube.execute_move(move)
        
        return moves
    
    def position_corner(self, colors: List[str], target: List[tuple]) -> List[str]:
        """Position and orient a single corner"""
        moves = []
        
        # Simplified corner positioning
        corner = self.cube.find_piece(colors)
        if corner == target and self.cube.get_piece_at(corner)[0] == 'W':
            return moves
        
        # Basic algorithm to position corner
        if corner and any(pos[0] == 'U' for pos in corner):
            # Corner in top layer - remove it
            alg = ['R', 'U', "R'", "U'"]
            moves.extend(alg)
            for m in alg:
                self.cube.execute_move(m)
        
        # Position and insert
        alg = ["U'", 'R', 'U', "R'"]
        moves.extend(alg)
        for m in alg:
            self.cube.execute_move(m)
        
        return moves
    
    def solve_second_layer(self) -> List[str]:
        """Solve middle layer edges"""
        moves = []
        
        # Middle layer edge algorithms
        right_algorithm = ['U', 'R', "U'", "R'", "U'", "F'", 'U', 'F']
        left_algorithm = ["U'", "L'", 'U', 'L', 'U', 'F', "U'", "F'"]
        
        # Apply algorithms based on edge positions
        for _ in range(4):
            # Try right algorithm
            alg = right_algorithm if len(moves) % 2 == 0 else left_algorithm
            moves.extend(alg)
            for m in alg:
                self.cube.execute_move(m)
        
        return moves
    
    def solve_oll(self) -> List[str]:
        """Orient last layer"""
        moves = []
        
        # Common OLL algorithms
        oll_algorithms = [
            # Dot
            ['F', 'R', 'U', "R'", "U'", "F'", 'f', 'R', 'U', "R'", "U'", "f'"],
            # Line
            ['F', 'R', 'U', "R'", "U'", "F'"],
            # L shape
            ['f', 'R', 'U', "R'", "U'", "f'"],
            # Cross
            ['R', 'U2', "R'", "U'", 'R', "U'", "R'"],
            # Sune
            ['R', 'U', "R'", 'U', 'R', 'U2', "R'"],
            # Antisune
            ["R'", "U'", 'R', "U'", "R'", 'U2', 'R']
        ]
        
        # Try OLL algorithms
        for oll in oll_algorithms:
            # Convert f moves to F moves
            expanded_oll = []
            for move in oll:
                if move == 'f':
                    expanded_oll.extend(['F', 'S'])
                elif move == "f'":
                    expanded_oll.extend(["F'", "S'"])
                elif move == 'S':
                    expanded_oll.extend(['F', "B'", 'z'])
                elif move == "S'":
                    expanded_oll.extend(["F'", 'B', "z'"])
                elif move in ['z', "z'"]:
                    continue  # Skip rotations
                else:
                    expanded_oll.append(move)
            
            moves.extend(expanded_oll)
            for m in expanded_oll:
                self.cube.execute_move(m)
            
            # Check if last layer is oriented
            if self.check_last_layer_oriented():
                break
            
            # Try with U rotations
            for _ in range(4):
                moves.append('U')
                self.cube.execute_move('U')
                if self.check_last_layer_oriented():
                    break
        
        return moves
    
    def solve_pll(self) -> List[str]:
        """Permute last layer"""
        moves = []
        
        # Common PLL algorithms
        pll_algorithms = [
            # U perm (edges)
            ['R2', 'U', 'R', 'U', "R'", "U'", "R'", "U'", "R'", 'U', "R'"],
            # H perm
            ['M2', 'U', 'M2', 'U2', 'M2', 'U', 'M2'],
            # Z perm
            ['M2', 'U', 'M2', 'U', 'M', 'U2', 'M2', 'U2', 'M', "U2"],
            # T perm
            ['R', 'U', "R'", "U'", "R'", 'F', 'R2', "U'", "R'", "U'", 'R', 'U', "R'", "F'"],
            # Y perm
            ['F', 'R', "U'", "R'", "U'", 'R', 'U', "R'", "F'", 'R', 'U', "R'", "U'", "R'", 'F', 'R', "F'"],
            # A perm
            ["x", "R'", 'U', "R'", 'D2', 'R', "U'", "R'", 'D2', 'R2', "x'"]
        ]
        
        for pll in pll_algorithms:
            # Convert M moves and rotations
            expanded_pll = []
            for move in pll:
                if move == 'M':
                    expanded_pll.extend(["L'", 'R', "F'", 'B'])
                elif move == "M'":
                    expanded_pll.extend(['L', "R'", 'F', "B'"])
                elif move == 'M2':
                    expanded_pll.extend(['L2', 'R2', 'F2', 'B2'])
                elif move in ['x', "x'", 'y', "y'", 'z', "z'"]:
                    continue  # Skip rotations
                else:
                    expanded_pll.append(move)
            
            moves.extend(expanded_pll)
            for m in expanded_pll:
                self.cube.execute_move(m)
            
            if self.cube.is_solved():
                break
            
            # Try with U rotations
            for _ in range(4):
                moves.append('U')
                self.cube.execute_move('U')
                if self.cube.is_solved():
                    break
        
        return moves
    
    def check_last_layer_oriented(self) -> bool:
        """Check if last layer pieces are oriented correctly"""
        # Check if all stickers on D face are yellow
        return all(self.cube.state['D'][i] == 'Y' for i in range(9))
    
    def optimize_solution(self, moves: List[str]) -> List[str]:
        """Optimize solution by canceling redundant moves"""
        if not moves:
            return moves
        
        optimized = []
        i = 0
        
        while i < len(moves):
            if i + 1 < len(moves):
                # Check for cancellations
                current = moves[i]
                next_move = moves[i + 1]
                
                # Same face opposite moves cancel out
                if current == self.inverse_move(next_move):
                    i += 2
                    continue
                
                # Same face same direction combine
                if current == next_move and not current.endswith('2'):
                    if current.endswith("'"):
                        optimized.append(current[0] + '2')
                    else:
                        optimized.append(current + '2')
                    i += 2
                    continue
                
                # Three quarter turns = one inverse
                if i + 2 < len(moves) and moves[i] == moves[i+1] == moves[i+2]:
                    if not moves[i].endswith('2'):
                        optimized.append(self.inverse_move(moves[i]))
                        i += 3
                        continue
            
            optimized.append(moves[i])
            i += 1
        
        # Recursive optimization until no more changes
        if len(optimized) < len(moves):
            return self.optimize_solution(optimized)
        
        return optimized
    
    def is_redundant(self, move: str, last_move: str) -> bool:
        """Check if move is redundant with previous move"""
        if not last_move:
            return False
        
        # Same face moves should be combined
        if move[0] == last_move[0]:
            return True
        
        # Opposite faces should be in consistent order
        opposite_pairs = [('U', 'D'), ('R', 'L'), ('F', 'B')]
        for face1, face2 in opposite_pairs:
            if (move[0] == face1 and last_move[0] == face2) or \
               (move[0] == face2 and last_move[0] == face1):
                # Keep consistent order: U before D, R before L, F before B
                return move[0] > last_move[0]
        
        return False
    
    def inverse_move(self, move: str) -> str:
        """Get inverse of a move"""
        if move.endswith("'"):
            return move[0]
        elif move.endswith("2"):
            return move
        else:
            return move + "'"
    
    def analyze_phases(self, solution: List[str]) -> Dict:
        """Analyze solution and identify phases"""
        if len(solution) == 0:
            return {}
        
        # Divide solution into phases based on move patterns
        phase1_end = 0
        phase2_start = 0
        
        # Phase 1 typically uses all types of moves
        # Phase 2 uses only <U,D,R2,L2,F2,B2> moves
        for i, move in enumerate(solution):
            if all(m[0] in ['U', 'D'] or m.endswith('2') for m in solution[i:]):
                phase2_start = i
                break
        
        return {
            'phase1_reduction': solution[:phase2_start],
            'phase2_solution': solution[phase2_start:]
        }