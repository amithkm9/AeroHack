# backend/models/cube.py
import random
from typing import List, Dict, Tuple, Optional
import copy

class Cube:
    """
    Optimized Rubik's Cube model with enhanced mechanics and validation
    """
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Reset cube to solved state"""
        self.state = {
            'U': ['W'] * 9,  # Up (White)
            'D': ['Y'] * 9,  # Down (Yellow)
            'F': ['G'] * 9,  # Front (Green)
            'B': ['B'] * 9,  # Back (Blue)
            'R': ['R'] * 9,  # Right (Red)
            'L': ['O'] * 9   # Left (Orange)
        }
        self.move_history = []
        self._validate_state()
        
    def get_state(self) -> Dict[str, List[str]]:
        """Get current cube state"""
        return copy.deepcopy(self.state)
    
    def set_state(self, new_state: Dict[str, List[str]]):
        """Set cube state with validation"""
        if self._is_valid_state(new_state):
            self.state = copy.deepcopy(new_state)
        else:
            print("⚠️ Invalid state provided, keeping current state")
    
    def setState(self, new_state: Dict[str, List[str]]):
        """Alias for set_state for compatibility"""
        self.set_state(new_state)
    
    def get_move_history(self) -> List[str]:
        """Get history of moves executed"""
        return self.move_history.copy()
    
    def _is_valid_state(self, state: Dict[str, List[str]]) -> bool:
        """Validate that a state is physically possible"""
        required_faces = {'U', 'D', 'F', 'B', 'R', 'L'}
        required_colors = {'W', 'Y', 'G', 'B', 'R', 'O'}
        
        # Check structure
        if not isinstance(state, dict):
            return False
        
        if set(state.keys()) != required_faces:
            return False
        
        # Check each face
        for face, stickers in state.items():
            if not isinstance(stickers, list) or len(stickers) != 9:
                return False
            
            # Check colors are valid
            for color in stickers:
                if color not in required_colors:
                    return False
        
        # Count color distribution (should be 9 of each)
        color_count = {color: 0 for color in required_colors}
        for face_stickers in state.values():
            for color in face_stickers:
                color_count[color] += 1
        
        for color, count in color_count.items():
            if count != 9:
                print(f"⚠️ Invalid color count for {color}: {count} (should be 9)")
                return False
        
        return True
    
    def _validate_state(self):
        """Validate current state"""
        if not self._is_valid_state(self.state):
            print("⚠️ Cube state is invalid!")
            self.reset()
    
    def rotate_face_clockwise(self, face: str):
        """Rotate a face 90 degrees clockwise with validation"""
        if face not in self.state:
            raise ValueError(f"Invalid face: {face}")
            
        f = self.state[face]
        # Create a copy of the face
        temp = f[:]
        
        # Rotate the face clockwise
        # 0 1 2     6 3 0
        # 3 4 5  => 7 4 1  
        # 6 7 8     8 5 2
        f[0] = temp[6]
        f[1] = temp[3]
        f[2] = temp[0]
        f[3] = temp[7]
        f[4] = temp[4]  # Center stays the same
        f[5] = temp[1]
        f[6] = temp[8]
        f[7] = temp[5]
        f[8] = temp[2]
    
    def execute_move(self, move: str):
        """Execute a move with enhanced validation and error handling"""
        if not isinstance(move, str) or not move:
            raise ValueError(f"Invalid move format: {move}")
        
        original_state = copy.deepcopy(self.state)
        
        try:
            if move == 'U':
                self._move_U()
            elif move == "U'":
                self._move_U_prime()
            elif move == 'U2':
                self._move_U()
                self._move_U()
            elif move == 'D':
                self._move_D()
            elif move == "D'":
                self._move_D_prime()
            elif move == 'D2':
                self._move_D()
                self._move_D()
            elif move == 'R':
                self._move_R()
            elif move == "R'":
                self._move_R_prime()
            elif move == 'R2':
                self._move_R()
                self._move_R()
            elif move == 'L':
                self._move_L()
            elif move == "L'":
                self._move_L_prime()
            elif move == 'L2':
                self._move_L()
                self._move_L()
            elif move == 'F':
                self._move_F()
            elif move == "F'":
                self._move_F_prime()
            elif move == 'F2':
                self._move_F()
                self._move_F()
            elif move == 'B':
                self._move_B()
            elif move == "B'":
                self._move_B_prime()
            elif move == 'B2':
                self._move_B()
                self._move_B()
            else:
                raise ValueError(f"Unknown move: {move}")
            
            # Validate state after move
            if not self._is_valid_state(self.state):
                print(f"⚠️ Move {move} resulted in invalid state, reverting...")
                self.state = original_state
                raise ValueError(f"Move {move} created invalid state")
            
            self.move_history.append(move)
            
        except Exception as e:
            print(f"❌ Error executing move {move}: {e}")
            self.state = original_state  # Revert to original state
            raise
    
    def executeMove(self, move: str):
        """Alias for execute_move for compatibility"""
        self.execute_move(move)
    
    # Enhanced move implementations with better error handling
    def _move_U(self):
        """Up face clockwise"""
        try:
            self.rotate_face_clockwise('U')
            # Save the front row
            temp = [self.state['F'][0], self.state['F'][1], self.state['F'][2]]
            # Front <- Right
            self.state['F'][0] = self.state['R'][0]
            self.state['F'][1] = self.state['R'][1]
            self.state['F'][2] = self.state['R'][2]
            # Right <- Back
            self.state['R'][0] = self.state['B'][0]
            self.state['R'][1] = self.state['B'][1]
            self.state['R'][2] = self.state['B'][2]
            # Back <- Left
            self.state['B'][0] = self.state['L'][0]
            self.state['B'][1] = self.state['L'][1]
            self.state['B'][2] = self.state['L'][2]
            # Left <- Front (temp)
            self.state['L'][0] = temp[0]
            self.state['L'][1] = temp[1]
            self.state['L'][2] = temp[2]
        except Exception as e:
            raise ValueError(f"Error in U move: {e}")
    
    def _move_U_prime(self):
        """Up face counter-clockwise"""
        self._move_U()
        self._move_U()
        self._move_U()
    
    def _move_D(self):
        """Down face clockwise"""
        try:
            self.rotate_face_clockwise('D')
            # Save the front row
            temp = [self.state['F'][6], self.state['F'][7], self.state['F'][8]]
            # Front <- Left
            self.state['F'][6] = self.state['L'][6]
            self.state['F'][7] = self.state['L'][7]
            self.state['F'][8] = self.state['L'][8]
            # Left <- Back
            self.state['L'][6] = self.state['B'][6]
            self.state['L'][7] = self.state['B'][7]
            self.state['L'][8] = self.state['B'][8]
            # Back <- Right
            self.state['B'][6] = self.state['R'][6]
            self.state['B'][7] = self.state['R'][7]
            self.state['B'][8] = self.state['R'][8]
            # Right <- Front (temp)
            self.state['R'][6] = temp[0]
            self.state['R'][7] = temp[1]
            self.state['R'][8] = temp[2]
        except Exception as e:
            raise ValueError(f"Error in D move: {e}")
    
    def _move_D_prime(self):
        """Down face counter-clockwise"""
        self._move_D()
        self._move_D()
        self._move_D()
    
    def _move_R(self):
        """Right face clockwise"""
        try:
            self.rotate_face_clockwise('R')
            # Save column
            temp = [self.state['F'][2], self.state['F'][5], self.state['F'][8]]
            # Front <- Down
            self.state['F'][2] = self.state['D'][2]
            self.state['F'][5] = self.state['D'][5]
            self.state['F'][8] = self.state['D'][8]
            # Down <- Back (note the reversal due to orientation)
            self.state['D'][2] = self.state['B'][6]
            self.state['D'][5] = self.state['B'][3]
            self.state['D'][8] = self.state['B'][0]
            # Back <- Up (note the reversal)
            self.state['B'][6] = self.state['U'][2]
            self.state['B'][3] = self.state['U'][5]
            self.state['B'][0] = self.state['U'][8]
            # Up <- Front (temp)
            self.state['U'][2] = temp[0]
            self.state['U'][5] = temp[1]
            self.state['U'][8] = temp[2]
        except Exception as e:
            raise ValueError(f"Error in R move: {e}")
    
    def _move_R_prime(self):
        """Right face counter-clockwise"""
        self._move_R()
        self._move_R()
        self._move_R()
    
    def _move_L(self):
        """Left face clockwise"""
        try:
            self.rotate_face_clockwise('L')
            # Save column
            temp = [self.state['F'][0], self.state['F'][3], self.state['F'][6]]
            # Front <- Up
            self.state['F'][0] = self.state['U'][0]
            self.state['F'][3] = self.state['U'][3]
            self.state['F'][6] = self.state['U'][6]
            # Up <- Back (note the reversal)
            self.state['U'][0] = self.state['B'][8]
            self.state['U'][3] = self.state['B'][5]
            self.state['U'][6] = self.state['B'][2]
            # Back <- Down (note the reversal)
            self.state['B'][8] = self.state['D'][0]
            self.state['B'][5] = self.state['D'][3]
            self.state['B'][2] = self.state['D'][6]
            # Down <- Front (temp)
            self.state['D'][0] = temp[0]
            self.state['D'][3] = temp[1]
            self.state['D'][6] = temp[2]
        except Exception as e:
            raise ValueError(f"Error in L move: {e}")
    
    def _move_L_prime(self):
        """Left face counter-clockwise"""
        self._move_L()
        self._move_L()
        self._move_L()
    
    def _move_F(self):
        """Front face clockwise"""
        try:
            self.rotate_face_clockwise('F')
            # Save row/column
            temp = [self.state['U'][6], self.state['U'][7], self.state['U'][8]]
            # Up <- Left (column to row)
            self.state['U'][6] = self.state['L'][8]
            self.state['U'][7] = self.state['L'][5]
            self.state['U'][8] = self.state['L'][2]
            # Left <- Down (row to column)
            self.state['L'][2] = self.state['D'][0]
            self.state['L'][5] = self.state['D'][1]
            self.state['L'][8] = self.state['D'][2]
            # Down <- Right (column to row)
            self.state['D'][0] = self.state['R'][6]
            self.state['D'][1] = self.state['R'][3]
            self.state['D'][2] = self.state['R'][0]
            # Right <- Up (temp) (row to column)
            self.state['R'][0] = temp[0]
            self.state['R'][3] = temp[1]
            self.state['R'][6] = temp[2]
        except Exception as e:
            raise ValueError(f"Error in F move: {e}")
    
    def _move_F_prime(self):
        """Front face counter-clockwise"""
        self._move_F()
        self._move_F()
        self._move_F()
    
    def _move_B(self):
        """Back face clockwise"""
        try:
            self.rotate_face_clockwise('B')
            # Save row
            temp = [self.state['U'][0], self.state['U'][1], self.state['U'][2]]
            # Up <- Right (column to row)
            self.state['U'][0] = self.state['R'][2]
            self.state['U'][1] = self.state['R'][5]
            self.state['U'][2] = self.state['R'][8]
            # Right <- Down (row to column)
            self.state['R'][2] = self.state['D'][8]
            self.state['R'][5] = self.state['D'][7]
            self.state['R'][8] = self.state['D'][6]
            # Down <- Left (column to row)
            self.state['D'][6] = self.state['L'][0]
            self.state['D'][7] = self.state['L'][3]
            self.state['D'][8] = self.state['L'][6]
            # Left <- Up (temp) (row to column)
            self.state['L'][0] = temp[2]
            self.state['L'][3] = temp[1]
            self.state['L'][6] = temp[0]
        except Exception as e:
            raise ValueError(f"Error in B move: {e}")
    
    def _move_B_prime(self):
        """Back face counter-clockwise"""
        self._move_B()
        self._move_B()
        self._move_B()
    
    def scramble(self, num_moves: int = 25) -> List[str]:
        """Enhanced scramble with better move distribution"""
        all_moves = ['U', "U'", 'U2', 'D', "D'", 'D2', 
                     'R', "R'", 'R2', 'L', "L'", 'L2', 
                     'F', "F'", 'F2', 'B', "B'", 'B2']
        scramble_moves = []
        last_face = ""
        face_count = {'U': 0, 'D': 0, 'F': 0, 'B': 0, 'R': 0, 'L': 0}
        
        for i in range(num_moves):
            # Avoid consecutive moves on same face and prevent too many moves on one face
            available_moves = []
            for move in all_moves:
                face = move[0]
                if face != last_face and face_count[face] < num_moves // 4:  # Max 25% of moves per face
                    available_moves.append(move)
            
            if not available_moves:  # Fallback if restrictions are too tight
                available_moves = [m for m in all_moves if m[0] != last_face]
            
            if not available_moves:  # Ultimate fallback
                available_moves = all_moves
            
            move = random.choice(available_moves)
            scramble_moves.append(move)
            
            try:
                self.execute_move(move)
                last_face = move[0]
                face_count[move[0]] += 1
            except Exception as e:
                print(f"⚠️ Scramble move {move} failed: {e}")
                # Continue with next move
                continue
        
        return scramble_moves
    
    def is_solved(self) -> bool:
        """Enhanced solved state check with validation"""
        try:
            # First validate the state is physically possible
            if not self._is_valid_state(self.state):
                return False
            
            # Check if each face has all stickers matching the center
            for face, stickers in self.state.items():
                center_color = stickers[4]  # Center piece
                if not all(color == center_color for color in stickers):
                    return False
            
            return True
        except Exception as e:
            print(f"⚠️ Error checking solved state: {e}")
            return False
    
    def isSolved(self) -> bool:
        """Alias for is_solved for compatibility"""
        return self.is_solved()
    
    def copy(self):
        """Create a deep copy of the cube"""
        new_cube = Cube()
        new_cube.state = copy.deepcopy(self.state)
        new_cube.move_history = self.move_history.copy()
        return new_cube
    
    def get_face_color(self, face: str) -> str:
        """Get the center color of a face"""
        if face in self.state:
            return self.state[face][4]
        return None
    
    def get_piece_at(self, face: str, position: int) -> str:
        """Get color of piece at specific position"""
        if face in self.state and 0 <= position <= 8:
            return self.state[face][position]
        return None
    
    def count_solved_pieces(self) -> Dict[str, int]:
        """Count how many pieces are in correct position for each face"""
        solved_count = {}
        
        for face, stickers in self.state.items():
            center_color = stickers[4]
            count = sum(1 for color in stickers if color == center_color)
            solved_count[face] = count
        
        return solved_count
    
    def get_solve_percentage(self) -> float:
        """Get percentage of cube that is solved"""
        solved_pieces = sum(self.count_solved_pieces().values())
        return (solved_pieces / 54) * 100  # 54 total pieces
    
    def analyze_state(self) -> Dict:
        """Analyze current cube state"""
        analysis = {
            'is_solved': self.is_solved(),
            'solve_percentage': self.get_solve_percentage(),
            'moves_made': len(self.move_history),
            'last_move': self.move_history[-1] if self.move_history else None,
            'face_analysis': {}
        }
        
        for face in ['U', 'D', 'F', 'B', 'R', 'L']:
            center_color = self.state[face][4]
            correct_pieces = sum(1 for color in self.state[face] if color == center_color)
            analysis['face_analysis'][face] = {
                'center_color': center_color,
                'correct_pieces': correct_pieces,
                'percentage': (correct_pieces / 9) * 100
            }
        
        return analysis
    
    def print_state(self):
        """Enhanced state printing with color indicators"""
        print("\n" + "="*50)
        print("🎲 CURRENT CUBE STATE")
        print("="*50)
        
        # Color mapping for better visualization
        color_symbols = {
            'W': '⬜', 'Y': '🟨', 'G': '🟩', 
            'B': '🟦', 'R': '🟥', 'O': '🟧'
        }
        
        def format_face(face_data):
            return [color_symbols.get(color, color) for color in face_data]
        
        # Print U face
        u_face = format_face(self.state['U'])
        print("      ", ' '.join(u_face[0:3]))
        print("      ", ' '.join(u_face[3:6]))
        print("      ", ' '.join(u_face[6:9]))
        print()
        
        # Print middle layer (L F R B)
        l_face = format_face(self.state['L'])
        f_face = format_face(self.state['F'])
        r_face = format_face(self.state['R'])
        b_face = format_face(self.state['B'])
        
        for i in range(3):
            row_start = i * 3
            row_end = row_start + 3
            print(' '.join(l_face[row_start:row_end]), 
                  ' '.join(f_face[row_start:row_end]),
                  ' '.join(r_face[row_start:row_end]),
                  ' '.join(b_face[row_start:row_end]))
        print()
        
        # Print D face
        d_face = format_face(self.state['D'])
        print("      ", ' '.join(d_face[0:3]))
        print("      ", ' '.join(d_face[3:6]))
        print("      ", ' '.join(d_face[6:9]))
        
        # Print analysis
        analysis = self.analyze_state()
        print("\n📊 ANALYSIS:")
        print(f"Solved: {'✅' if analysis['is_solved'] else '❌'} ({analysis['solve_percentage']:.1f}%)")
        print(f"Moves: {analysis['moves_made']}")
        if analysis['last_move']:
            print(f"Last move: {analysis['last_move']}")
        
        print("\n🎯 Face Status:")
        for face, data in analysis['face_analysis'].items():
            status = '✅' if data['percentage'] == 100 else f"{data['percentage']:.0f}%"
            print(f"  {face}: {status} ({data['correct_pieces']}/9)")
        
        print("="*50)
    
    def validate_solution(self, moves: List[str]) -> bool:
        """Validate that a sequence of moves would solve the cube"""
        if self.is_solved():
            return len(moves) == 0
        
        # Create a test cube
        test_cube = self.copy()
        
        try:
            for move in moves:
                test_cube.execute_move(move)
            return test_cube.is_solved()
        except Exception as e:
            print(f"⚠️ Solution validation failed: {e}")
            return False
    
    def apply_moves(self, moves: List[str]) -> bool:
        """Apply a sequence of moves with validation"""
        if not moves:
            return True
        
        original_state = copy.deepcopy(self.state)
        original_history = self.move_history.copy()
        
        try:
            for move in moves:
                self.execute_move(move)
            return True
        except Exception as e:
            print(f"⚠️ Failed to apply moves: {e}")
            # Restore original state
            self.state = original_state
            self.move_history = original_history
            return False
    
    def get_statistics(self) -> Dict:
        """Get detailed cube statistics"""
        return {
            'total_moves': len(self.move_history),
            'is_solved': self.is_solved(),
            'solve_percentage': self.get_solve_percentage(),
            'face_completion': self.count_solved_pieces(),
            'move_distribution': self._get_move_distribution(),
            'state_valid': self._is_valid_state(self.state)
        }
    
    def _get_move_distribution(self) -> Dict[str, int]:
        """Get distribution of moves by face"""
        distribution = {'U': 0, 'D': 0, 'F': 0, 'B': 0, 'R': 0, 'L': 0}
        
        for move in self.move_history:
            if move and move[0] in distribution:
                distribution[move[0]] += 1
        
        return distribution