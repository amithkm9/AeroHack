# backend/models/cube.py
import random
from typing import List, Dict, Tuple, Optional
import copy

class Cube:
    """
    Rubik's Cube model with all necessary operations
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
        # Rotate corners
        temp = [f[0], f[2], f[8], f[6]]
        f[0], f[2], f[8], f[6] = temp[3], temp[0], temp[1], temp[2]
        # Rotate edges
        temp = [f[1], f[5], f[7], f[3]]
        f[1], f[5], f[7], f[3] = temp[3], temp[0], temp[1], temp[2]
    
    def execute_move(self, move: str):
        """Execute a move in standard notation"""
        # Define all basic moves
        moves = {
            'U': self._move_U,
            "U'": self._move_U_prime,
            'U2': lambda: [self._move_U() for _ in range(2)],
            'D': self._move_D,
            "D'": self._move_D_prime,
            'D2': lambda: [self._move_D() for _ in range(2)],
            'R': self._move_R,
            "R'": self._move_R_prime,
            'R2': lambda: [self._move_R() for _ in range(2)],
            'L': self._move_L,
            "L'": self._move_L_prime,
            'L2': lambda: [self._move_L() for _ in range(2)],
            'F': self._move_F,
            "F'": self._move_F_prime,
            'F2': lambda: [self._move_F() for _ in range(2)],
            'B': self._move_B,
            "B'": self._move_B_prime,
            'B2': lambda: [self._move_B() for _ in range(2)]
        }
        
        if move in moves:
            moves[move]()
            self.move_history.append(move)
        else:
            raise ValueError(f"Invalid move: {move}")
    
    def _move_U(self):
        """Up face clockwise"""
        self.rotate_face_clockwise('U')
        temp = self.state['F'][0:3]
        self.state['F'][0:3] = self.state['R'][0:3]
        self.state['R'][0:3] = self.state['B'][0:3]
        self.state['B'][0:3] = self.state['L'][0:3]
        self.state['L'][0:3] = temp
    
    def _move_U_prime(self):
        """Up face counter-clockwise"""
        for _ in range(3):
            self._move_U()
    
    def _move_D(self):
        """Down face clockwise"""
        self.rotate_face_clockwise('D')
        temp = self.state['F'][6:9]
        self.state['F'][6:9] = self.state['L'][6:9]
        self.state['L'][6:9] = self.state['B'][6:9]
        self.state['B'][6:9] = self.state['R'][6:9]
        self.state['R'][6:9] = temp
    
    def _move_D_prime(self):
        """Down face counter-clockwise"""
        for _ in range(3):
            self._move_D()
    
    def _move_R(self):
        """Right face clockwise"""
        self.rotate_face_clockwise('R')
        temp = [self.state['F'][2], self.state['F'][5], self.state['F'][8]]
        self.state['F'][2], self.state['F'][5], self.state['F'][8] = \
            self.state['D'][2], self.state['D'][5], self.state['D'][8]
        self.state['D'][2], self.state['D'][5], self.state['D'][8] = \
            self.state['B'][6], self.state['B'][3], self.state['B'][0]
        self.state['B'][6], self.state['B'][3], self.state['B'][0] = \
            self.state['U'][2], self.state['U'][5], self.state['U'][8]
        self.state['U'][2], self.state['U'][5], self.state['U'][8] = temp
    
    def _move_R_prime(self):
        """Right face counter-clockwise"""
        for _ in range(3):
            self._move_R()
    
    def _move_L(self):
        """Left face clockwise"""
        self.rotate_face_clockwise('L')
        temp = [self.state['F'][0], self.state['F'][3], self.state['F'][6]]
        self.state['F'][0], self.state['F'][3], self.state['F'][6] = \
            self.state['U'][0], self.state['U'][3], self.state['U'][6]
        self.state['U'][0], self.state['U'][3], self.state['U'][6] = \
            self.state['B'][8], self.state['B'][5], self.state['B'][2]
        self.state['B'][8], self.state['B'][5], self.state['B'][2] = \
            self.state['D'][0], self.state['D'][3], self.state['D'][6]
        self.state['D'][0], self.state['D'][3], self.state['D'][6] = temp
    
    def _move_L_prime(self):
        """Left face counter-clockwise"""
        for _ in range(3):
            self._move_L()
    
    def _move_F(self):
        """Front face clockwise"""
        self.rotate_face_clockwise('F')
        temp = [self.state['U'][6], self.state['U'][7], self.state['U'][8]]
        self.state['U'][6], self.state['U'][7], self.state['U'][8] = \
            self.state['L'][8], self.state['L'][5], self.state['L'][2]
        self.state['L'][8], self.state['L'][5], self.state['L'][2] = \
            self.state['D'][2], self.state['D'][1], self.state['D'][0]
        self.state['D'][2], self.state['D'][1], self.state['D'][0] = \
            self.state['R'][0], self.state['R'][3], self.state['R'][6]
        self.state['R'][0], self.state['R'][3], self.state['R'][6] = temp
    
    def _move_F_prime(self):
        """Front face counter-clockwise"""
        for _ in range(3):
            self._move_F()
    
    def _move_B(self):
        """Back face clockwise"""
        self.rotate_face_clockwise('B')
        temp = [self.state['U'][0], self.state['U'][1], self.state['U'][2]]
        self.state['U'][0], self.state['U'][1], self.state['U'][2] = \
            self.state['R'][2], self.state['R'][5], self.state['R'][8]
        self.state['R'][2], self.state['R'][5], self.state['R'][8] = \
            self.state['D'][8], self.state['D'][7], self.state['D'][6]
        self.state['D'][8], self.state['D'][7], self.state['D'][6] = \
            self.state['L'][6], self.state['L'][3], self.state['L'][0]
        self.state['L'][6], self.state['L'][3], self.state['L'][0] = temp
    
    def _move_B_prime(self):
        """Back face counter-clockwise"""
        for _ in range(3):
            self._move_B()
    
    def scramble(self, num_moves: int = 25) -> List[str]:
        """Scramble the cube with random moves"""
        moves = ['U', "U'", 'D', "D'", 'R', "R'", 'L', "L'", 'F', "F'", 'B', "B'"]
        scramble_moves = []
        last_face = ""
        
        for _ in range(num_moves):
            # Avoid consecutive moves on same face
            available_moves = [m for m in moves if m[0] != last_face]
            move = random.choice(available_moves)
            scramble_moves.append(move)
            self.execute_move(move)
            last_face = move[0]
        
        return scramble_moves
    
    def is_solved(self) -> bool:
        """Check if cube is in solved state"""
        for face, stickers in self.state.items():
            center_color = stickers[4]
            if not all(color == center_color for color in stickers):
                return False
        return True
    
    def find_piece(self, colors: List[str]) -> Optional[List[Tuple[str, int]]]:
        """Find a piece with given colors and return its position"""
        # Implementation for finding pieces
        # This is used by solvers to locate specific pieces
        
        # Edge pieces (2 colors)
        if len(colors) == 2:
            edges = [
                [('U', 1), ('B', 1)], [('U', 3), ('L', 1)], 
                [('U', 5), ('R', 1)], [('U', 7), ('F', 1)],
                [('D', 1), ('F', 7)], [('D', 3), ('L', 7)], 
                [('D', 5), ('R', 7)], [('D', 7), ('B', 7)],
                [('F', 3), ('L', 5)], [('F', 5), ('R', 3)],
                [('B', 3), ('R', 5)], [('B', 5), ('L', 3)]
            ]
            
            for edge in edges:
                piece_colors = [self.state[pos[0]][pos[1]] for pos in edge]
                if set(piece_colors) == set(colors):
                    return edge
        
        # Corner pieces (3 colors)
        elif len(colors) == 3:
            corners = [
                [('U', 0), ('L', 0), ('B', 2)], [('U', 2), ('B', 0), ('R', 2)],
                [('U', 6), ('F', 0), ('L', 2)], [('U', 8), ('R', 0), ('F', 2)],
                [('D', 0), ('L', 6), ('F', 6)], [('D', 2), ('F', 8), ('R', 6)],
                [('D', 6), ('B', 6), ('L', 8)], [('D', 8), ('R', 8), ('B', 8)]
            ]
            
            for corner in corners:
                piece_colors = [self.state[pos[0]][pos[1]] for pos in corner]
                if set(piece_colors) == set(colors):
                    return corner
        
        return None
    
    def get_piece_at(self, positions: List[Tuple[str, int]]) -> List[str]:
        """Get colors of piece at given positions"""
        return [self.state[face][pos] for face, pos in positions]
    
    def copy(self):
        """Create a deep copy of the cube"""
        new_cube = Cube()
        new_cube.state = copy.deepcopy(self.state)
        new_cube.move_history = self.move_history.copy()
        return new_cube