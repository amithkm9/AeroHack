# backend/models/cube.py
import random
from typing import List, Dict, Tuple, Optional
import copy

class Cube:
    """
    Rubik's Cube model with all necessary operations
    Fixed rotation logic for proper cube mechanics
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
    
    def get_state(self) -> Dict[str, List[str]]:
        """Get current cube state"""
        return copy.deepcopy(self.state)
    
    def get_move_history(self) -> List[str]:
        """Get history of moves executed"""
        return self.move_history.copy()
    
    def rotate_face_clockwise(self, face: str):
        """Rotate a face 90 degrees clockwise"""
        f = self.state[face]
        # Create a copy of the face
        temp = f[:]
        
        # Rotate the face
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
        """Execute a move in standard notation"""
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
            raise ValueError(f"Invalid move: {move}")
        
        self.move_history.append(move)
    
    def _move_U(self):
        """Up face clockwise"""
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
    
    def _move_U_prime(self):
        """Up face counter-clockwise"""
        # Three clockwise rotations = one counter-clockwise
        self._move_U()
        self._move_U()
        self._move_U()
    
    def _move_D(self):
        """Down face clockwise"""
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
    
    def _move_D_prime(self):
        """Down face counter-clockwise"""
        self._move_D()
        self._move_D()
        self._move_D()
    
    def _move_R(self):
        """Right face clockwise"""
        self.rotate_face_clockwise('R')
        # Save column
        temp = [self.state['F'][2], self.state['F'][5], self.state['F'][8]]
        # Front <- Down
        self.state['F'][2] = self.state['D'][2]
        self.state['F'][5] = self.state['D'][5]
        self.state['F'][8] = self.state['D'][8]
        # Down <- Back (note the reversal due to rotation)
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
    
    def _move_R_prime(self):
        """Right face counter-clockwise"""
        self._move_R()
        self._move_R()
        self._move_R()
    
    def _move_L(self):
        """Left face clockwise"""
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
    
    def _move_L_prime(self):
        """Left face counter-clockwise"""
        self._move_L()
        self._move_L()
        self._move_L()
    
    def _move_F(self):
        """Front face clockwise"""
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
    
    def _move_F_prime(self):
        """Front face counter-clockwise"""
        self._move_F()
        self._move_F()
        self._move_F()
    
    def _move_B(self):
        """Back face clockwise"""
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
    
    def _move_B_prime(self):
        """Back face counter-clockwise"""
        self._move_B()
        self._move_B()
        self._move_B()
    
    def scramble(self, num_moves: int = 25) -> List[str]:
        """Scramble the cube with random moves"""
        all_moves = ['U', "U'", 'U2', 'D', "D'", 'D2', 
                     'R', "R'", 'R2', 'L', "L'", 'L2', 
                     'F', "F'", 'F2', 'B', "B'", 'B2']
        scramble_moves = []
        last_face = ""
        
        for _ in range(num_moves):
            # Avoid consecutive moves on same face
            available_moves = [m for m in all_moves if m[0] != last_face]
            move = random.choice(available_moves)
            scramble_moves.append(move)
            self.execute_move(move)
            last_face = move[0]
        
        return scramble_moves
    
    def is_solved(self) -> bool:
        """Check if cube is in solved state"""
        for face, stickers in self.state.items():
            # All stickers on a face should match the center color
            center_color = stickers[4]
            if not all(color == center_color for color in stickers):
                return False
        return True
    
    def copy(self):
        """Create a deep copy of the cube"""
        new_cube = Cube()
        new_cube.state = copy.deepcopy(self.state)
        new_cube.move_history = self.move_history.copy()
        return new_cube
    
    def print_state(self):
        """Print the current state of the cube for debugging"""
        print("\nCurrent Cube State:")
        print("       ", self.state['U'][0:3])
        print("       ", self.state['U'][3:6])
        print("       ", self.state['U'][6:9])
        print()
        print(self.state['L'][0:3], self.state['F'][0:3], self.state['R'][0:3], self.state['B'][0:3])
        print(self.state['L'][3:6], self.state['F'][3:6], self.state['R'][3:6], self.state['B'][3:6])
        print(self.state['L'][6:9], self.state['F'][6:9], self.state['R'][6:9], self.state['B'][6:9])
        print()
        print("       ", self.state['D'][0:3])
        print("       ", self.state['D'][3:6])
        print("       ", self.state['D'][6:9])