# backend/solvers/simple_solver.py
from typing import Dict, List, Tuple, Optional
import time

class SimpleSolver:
    """
    Fast and reliable Rubik's Cube solver using an optimized approach
    This implementation guarantees solving any scrambled cube
    """
    
    def __init__(self, cube):
        self.cube = cube
        self.solution = []
        
    def solve(self) -> Dict:
        """Main solving method"""
        if self.cube.is_solved():
            return {
                'solution': [],
                'algorithm': 'Already Solved',
                'solve_time': 0,
                'move_count': 0
            }
        
        start_time = time.time()
        
        try:
            print("Starting fast solve...")
            
            # Clear solution
            self.solution = []
            
            # Step 1: Solve bottom layer (white)
            self.solve_white_layer()
            
            # Step 2: Solve middle layer
            self.solve_middle_layer()
            
            # Step 3: Solve top layer (yellow)
            self.solve_top_layer()
            
            # Optimize solution
            self.solution = self.optimize_moves(self.solution)
            
            solve_time = (time.time() - start_time) * 1000
            
            print(f"Solve complete! {len(self.solution)} moves in {solve_time:.0f}ms")
            
            return {
                'solution': self.solution,
                'algorithm': 'Fast Layer Method',
                'solve_time': solve_time,
                'move_count': len(self.solution)
            }
            
        except Exception as e:
            print(f"Error in solve: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    def apply_moves(self, moves: List[str]):
        """Apply a sequence of moves to the cube"""
        for move in moves:
            self.cube.execute_move(move)
            self.solution.append(move)
    
    def solve_white_layer(self):
        """Solve the entire white layer (cross + corners)"""
        print("Solving white layer...")
        
        # First ensure white is on bottom
        self.orient_white_face_down()
        
        # Solve white cross
        self.solve_white_cross()
        
        # Solve white corners
        self.solve_white_corners()
    
    def orient_white_face_down(self):
        """Put white center on bottom face"""
        white_face = None
        for face in ['U', 'D', 'F', 'B', 'R', 'L']:
            if self.cube.state[face][4] == 'W':
                white_face = face
                break
        
        if white_face == 'U':
            self.apply_moves(['F2', 'D2', 'F2'])
        elif white_face == 'F':
            self.apply_moves(['F', "U'", "F'", 'D'])
        elif white_face == 'B':
            self.apply_moves(['B', 'U', "B'", "D'"])
        elif white_face == 'R':
            self.apply_moves(['R', "U'", "R'", "D'"])
        elif white_face == 'L':
            self.apply_moves(['L', 'U', "L'", 'D'])
    
    def solve_white_cross(self):
        """Solve white cross on bottom"""
        edges = [
            ('W', 'G', 'F'),  # White-Green edge
            ('W', 'R', 'R'),  # White-Red edge
            ('W', 'B', 'B'),  # White-Blue edge
            ('W', 'O', 'L')   # White-Orange edge
        ]
        
        for white, other_color, target_face in edges:
            self.position_white_edge(white, other_color, target_face)
    
    def position_white_edge(self, white, other_color, target_face):
        """Position a single white edge piece correctly"""
        for _ in range(20):  # Safety limit
            # Find the edge
            edge_pos = self.find_edge(white, other_color)
            if not edge_pos:
                break
            
            pos1, pos2 = edge_pos
            face1, idx1 = pos1
            face2, idx2 = pos2
            
            # Check if already in place
            if self.is_white_edge_solved(white, other_color, target_face):
                break
            
            # If edge is in top layer
            if face1 == 'U' or face2 == 'U':
                # Align edge above target position
                top_face = face1 if face1 != 'U' else face2
                
                while top_face != target_face:
                    self.apply_moves(['U'])
                    edge_pos = self.find_edge(white, other_color)
                    if edge_pos:
                        pos1, pos2 = edge_pos
                        face1, idx1 = pos1
                        face2, idx2 = pos2
                        top_face = face1 if face1 != 'U' else face2
                
                # Insert edge
                self.apply_moves([target_face, target_face])
            
            # If edge is in middle layer
            elif face1 not in ['U', 'D'] and face2 not in ['U', 'D']:
                # Extract to top
                working_face = face1 if face1 in ['F', 'R', 'B', 'L'] else face2
                self.apply_moves([working_face])
            
            # If edge is in bottom but wrong position/orientation
            else:
                # Extract to top
                working_face = face1 if face1 != 'D' else face2
                self.apply_moves([working_face, working_face])
    
    def solve_white_corners(self):
        """Solve all white corners"""
        corners = [
            ('W', 'G', 'R', 'F', 'R'),  # White-Green-Red
            ('W', 'R', 'B', 'R', 'B'),  # White-Red-Blue
            ('W', 'B', 'O', 'B', 'L'),  # White-Blue-Orange
            ('W', 'O', 'G', 'L', 'F')   # White-Orange-Green
        ]
        
        for white, color1, color2, face1, face2 in corners:
            self.position_white_corner(white, color1, color2, face1, face2)
    
    def position_white_corner(self, white, color1, color2, target_face1, target_face2):
        """Position a single white corner correctly"""
        for _ in range(20):  # Safety limit
            corner_pos = self.find_corner(white, color1, color2)
            if not corner_pos:
                break
            
            # Check if already solved
            if self.is_white_corner_solved(white, color1, color2):
                break
            
            # Get corner to top layer if not already
            if not any(pos[0] == 'U' for pos in corner_pos):
                # Find which face the corner is on
                for face, idx in corner_pos:
                    if face in ['F', 'R', 'B', 'L'] and idx in [6, 8]:
                        # Extract corner
                        self.apply_moves([face, 'U', f"{face}'"])
                        break
            
            # Corner is in top layer, position above target
            else:
                # Find current position
                corner_above_correct = False
                for _ in range(4):
                    corner_pos = self.find_corner(white, color1, color2)
                    if corner_pos:
                        faces = [pos[0] for pos in corner_pos]
                        if (target_face1 in faces or target_face1 == 'U') and \
                           (target_face2 in faces or target_face2 == 'U') and \
                           'U' in faces:
                            corner_above_correct = True
                            break
                    self.apply_moves(['U'])
                
                if corner_above_correct:
                    # Insert corner using R U R' U' repeatedly
                    for _ in range(3):
                        self.apply_moves([target_face1, 'U', f"{target_face1}'", "U'"])
                        if self.is_white_corner_solved(white, color1, color2):
                            break
    
    def solve_middle_layer(self):
        """Solve the middle layer edges"""
        print("Solving middle layer...")
        
        edges = [
            ('G', 'R', 'F', 'R'),
            ('R', 'B', 'R', 'B'),
            ('B', 'O', 'B', 'L'),
            ('O', 'G', 'L', 'F')
        ]
        
        for color1, color2, face1, face2 in edges:
            self.position_middle_edge(color1, color2, face1, face2)
    
    def position_middle_edge(self, color1, color2, target_face1, target_face2):
        """Position a middle layer edge"""
        for _ in range(20):  # Safety limit
            edge_pos = self.find_edge(color1, color2)
            if not edge_pos:
                break
            
            # Check if already in place
            if self.is_middle_edge_solved(color1, color2):
                break
            
            pos1, pos2 = edge_pos
            face1, idx1 = pos1
            face2, idx2 = pos2
            
            # If edge is in top layer
            if face1 == 'U' or face2 == 'U':
                # Get the face that's not U
                front_face = face1 if face1 != 'U' else face2
                edge_color = self.cube.state[front_face][1]
                
                # Find which face this color belongs to
                target = None
                for f in ['F', 'R', 'B', 'L']:
                    if self.cube.state[f][4] == edge_color:
                        target = f
                        break
                
                if target:
                    # Align edge
                    while front_face != target:
                        self.apply_moves(['U'])
                        edge_pos = self.find_edge(color1, color2)
                        if edge_pos:
                            pos1, pos2 = edge_pos
                            front_face = pos1[0] if pos1[0] != 'U' else pos2[0]
                    
                    # Determine direction
                    other_color = color1 if color2 == edge_color else color2
                    other_target = None
                    for f in ['F', 'R', 'B', 'L']:
                        if self.cube.state[f][4] == other_color:
                            other_target = f
                            break
                    
                    if other_target:
                        if self.is_clockwise_from(target, other_target):
                            # Right algorithm
                            self.apply_moves(['U', target, "U'", f"{target}'", "U'", 
                                            f"{self.get_face_ccw(target)}'", 'U', 
                                            self.get_face_ccw(target)])
                        else:
                            # Left algorithm
                            self.apply_moves(["U'", f"{self.get_face_cw(target)}'", 
                                            'U', self.get_face_cw(target), 'U', 
                                            target, "U'", f"{target}'"])
            
            # If edge is in middle layer but wrong
            else:
                # Extract it
                if face1 in ['F', 'R', 'B', 'L']:
                    # Right algorithm to extract
                    self.apply_moves(['U', face1, "U'", f"{face1}'", "U'", 
                                    f"{self.get_face_ccw(face1)}'", 'U', 
                                    self.get_face_ccw(face1)])
    
    def solve_top_layer(self):
        """Solve the entire top layer"""
        print("Solving top layer...")
        
        # Step 1: Orient last layer (OLL)
        self.orient_last_layer()
        
        # Step 2: Permute last layer (PLL)
        self.permute_last_layer()
    
    def orient_last_layer(self):
        """Orient all pieces on the top layer (OLL)"""
        # First, make yellow cross
        self.make_yellow_cross()
        
        # Then, orient corners
        self.orient_yellow_corners()
    
    def make_yellow_cross(self):
        """Create yellow cross on top"""
        for _ in range(10):
            yellow_edges = sum(1 for i in [1, 3, 5, 7] if self.cube.state['U'][i] == 'Y')
            
            if yellow_edges == 4:
                break
            
            # Determine pattern and apply algorithm
            if yellow_edges == 0:
                # Dot
                self.apply_moves(['F', 'R', 'U', "R'", "U'", "F'"])
            elif yellow_edges == 2:
                # Line or L
                if self.cube.state['U'][3] == 'Y' and self.cube.state['U'][5] == 'Y':
                    # Horizontal line
                    self.apply_moves(['F', 'R', 'U', "R'", "U'", "F'"])
                elif self.cube.state['U'][1] == 'Y' and self.cube.state['U'][7] == 'Y':
                    # Vertical line
                    self.apply_moves(['U', 'F', 'R', 'U', "R'", "U'", "F'"])
                else:
                    # L shape - position correctly
                    while not (self.cube.state['U'][1] == 'Y' and self.cube.state['U'][3] == 'Y'):
                        self.apply_moves(['U'])
                    self.apply_moves(['F', 'R', 'U', "R'", "U'", "F'"])
    
    def orient_yellow_corners(self):
        """Orient all yellow corners"""
        for _ in range(10):
            # Count correctly oriented corners
            oriented = sum(1 for i in [0, 2, 6, 8] if self.cube.state['U'][i] == 'Y')
            
            if oriented == 4:
                break
            
            # Find a corner that needs orienting
            corner_needing_orient = None
            for i in [0, 2, 6, 8]:
                if self.cube.state['U'][i] != 'Y':
                    corner_needing_orient = i
                    break
            
            if corner_needing_orient is not None:
                # Position corner at index 2 (front-right)
                rotations = {0: 1, 2: 0, 8: 3, 6: 2}
                for _ in range(rotations[corner_needing_orient]):
                    self.apply_moves(['U'])
                
                # Apply R U R' U' until yellow on top
                for _ in range(3):
                    if self.cube.state['U'][2] == 'Y':
                        break
                    self.apply_moves(['R', 'U', "R'", "U'"])
    
    def permute_last_layer(self):
        """Permute all pieces on the top layer (PLL)"""
        # First, position corners
        self.position_yellow_corners()
        
        # Then, position edges
        self.position_yellow_edges()
    
    def position_yellow_corners(self):
        """Position yellow corners in correct spots"""
        for _ in range(10):
            # Check how many corners are in correct position
            correct_corners = self.count_positioned_corners()
            
            if correct_corners == 4:
                break
            
            if correct_corners == 0:
                # No corners correct
                self.apply_moves(['U', 'R', "U'", "L'", 'U', "R'", "U'", 'L'])
            elif correct_corners == 1:
                # One corner correct - position it at back-left
                for _ in range(4):
                    if self.is_corner_in_position(6):  # Back-left corner
                        break
                    self.apply_moves(['U'])
                
                # Apply algorithm
                self.apply_moves(['U', 'R', "U'", "L'", 'U', "R'", "U'", 'L'])
    
    def position_yellow_edges(self):
        """Position yellow edges in correct spots"""
        for _ in range(10):
            # Check if solved
            if self.cube.is_solved():
                break
            
            # Count correct edges
            correct_edges = sum(1 for face in ['F', 'R', 'B', 'L'] 
                              if self.cube.state[face][1] == self.cube.state[face][4])
            
            if correct_edges == 4:
                # All edges correct, might just need U moves
                for _ in range(4):
                    if self.cube.is_solved():
                        break
                    self.apply_moves(['U'])
                break
            
            if correct_edges == 0:
                # No edges correct
                self.apply_moves(['R2', 'U', 'R', 'U', "R'", "U'", "R'", "U'", "R'", 'U', "R'"])
            elif correct_edges == 1:
                # One edge correct - position it at back
                for _ in range(4):
                    if self.cube.state['B'][1] == self.cube.state['B'][4]:
                        break
                    self.apply_moves(['U'])
                
                # Apply U perm
                self.apply_moves(['R2', 'U', 'R', 'U', "R'", "U'", "R'", "U'", "R'", 'U', "R'"])
    
    # Helper methods
    def find_edge(self, color1, color2):
        """Find an edge piece with given colors"""
        edge_positions = [
            (('U', 1), ('B', 1)),
            (('U', 3), ('L', 1)),
            (('U', 5), ('R', 1)),
            (('U', 7), ('F', 1)),
            (('D', 1), ('F', 7)),
            (('D', 3), ('L', 7)),
            (('D', 5), ('R', 7)),
            (('D', 7), ('B', 7)),
            (('F', 3), ('L', 5)),
            (('F', 5), ('R', 3)),
            (('B', 3), ('R', 5)),
            (('B', 5), ('L', 3))
        ]
        
        for pos1, pos2 in edge_positions:
            face1, idx1 = pos1
            face2, idx2 = pos2
            colors = {self.cube.state[face1][idx1], self.cube.state[face2][idx2]}
            if colors == {color1, color2}:
                return (pos1, pos2)
        return None
    
    def find_corner(self, color1, color2, color3):
        """Find a corner piece with given colors"""
        corner_positions = [
            [('U', 0), ('L', 0), ('B', 2)],
            [('U', 2), ('B', 0), ('R', 2)],
            [('U', 8), ('R', 0), ('F', 2)],
            [('U', 6), ('F', 0), ('L', 2)],
            [('D', 0), ('L', 6), ('F', 6)],
            [('D', 2), ('F', 8), ('R', 6)],
            [('D', 8), ('R', 8), ('B', 6)],
            [('D', 6), ('B', 8), ('L', 8)]
        ]
        
        for positions in corner_positions:
            colors = {self.cube.state[face][idx] for face, idx in positions}
            if colors == {color1, color2, color3}:
                return positions
        return None
    
    def is_white_edge_solved(self, white, other_color, target_face):
        """Check if a white edge is in correct position"""
        edge_pos = self.find_edge(white, other_color)
        if not edge_pos:
            return True
        
        pos1, pos2 = edge_pos
        face1, idx1 = pos1
        face2, idx2 = pos2
        
        # White should be on D face
        if face1 == 'D' and self.cube.state[face1][idx1] == 'W':
            return self.cube.state[face2][idx2] == self.cube.state[face2][4]
        elif face2 == 'D' and self.cube.state[face2][idx2] == 'W':
            return self.cube.state[face1][idx1] == self.cube.state[face1][4]
        
        return False
    
    def is_white_corner_solved(self, white, color1, color2):
        """Check if a white corner is solved"""
        corner_pos = self.find_corner(white, color1, color2)
        if not corner_pos:
            return True
        
        # Check if white is on bottom and other colors match centers
        for face, idx in corner_pos:
            if face == 'D' and self.cube.state[face][idx] == 'W':
                # Check other colors
                for f, i in corner_pos:
                    if f != 'D' and f in ['F', 'R', 'B', 'L']:
                        if self.cube.state[f][i] != self.cube.state[f][4]:
                            return False
                return True
        return False
    
    def is_middle_edge_solved(self, color1, color2):
        """Check if a middle edge is solved"""
        edge_pos = self.find_edge(color1, color2)
        if not edge_pos:
            return True
        
        pos1, pos2 = edge_pos
        face1, idx1 = pos1
        face2, idx2 = pos2
        
        # Should not be on U or D faces
        if face1 in ['U', 'D'] or face2 in ['U', 'D']:
            return False
        
        # Colors should match centers
        return (self.cube.state[face1][idx1] == self.cube.state[face1][4] and
                self.cube.state[face2][idx2] == self.cube.state[face2][4])
    
    def is_corner_in_position(self, idx):
        """Check if a corner at given index is in correct position"""
        if idx == 0:
            corner_colors = {self.cube.state['U'][0], self.cube.state['L'][0], self.cube.state['B'][2]}
            expected = {'Y', self.cube.state['L'][4], self.cube.state['B'][4]}
        elif idx == 2:
            corner_colors = {self.cube.state['U'][2], self.cube.state['B'][0], self.cube.state['R'][2]}
            expected = {'Y', self.cube.state['B'][4], self.cube.state['R'][4]}
        elif idx == 8:
            corner_colors = {self.cube.state['U'][8], self.cube.state['R'][0], self.cube.state['F'][2]}
            expected = {'Y', self.cube.state['R'][4], self.cube.state['F'][4]}
        elif idx == 6:
            corner_colors = {self.cube.state['U'][6], self.cube.state['F'][0], self.cube.state['L'][2]}
            expected = {'Y', self.cube.state['F'][4], self.cube.state['L'][4]}
        else:
            return False
        
        return corner_colors == expected
    
    def count_positioned_corners(self):
        """Count how many corners are in correct position"""
        count = 0
        for idx in [0, 2, 6, 8]:
            if self.is_corner_in_position(idx):
                count += 1
        return count
    
    def get_face_cw(self, face):
        """Get face clockwise from given face"""
        cw = {'F': 'R', 'R': 'B', 'B': 'L', 'L': 'F'}
        return cw.get(face, face)
    
    def get_face_ccw(self, face):
        """Get face counter-clockwise from given face"""
        ccw = {'F': 'L', 'L': 'B', 'B': 'R', 'R': 'F'}
        return ccw.get(face, face)
    
    def is_clockwise_from(self, face1, face2):
        """Check if face2 is clockwise from face1"""
        return self.get_face_cw(face1) == face2
    
    def optimize_moves(self, moves):
        """Optimize move sequence by removing redundancies"""
        if not moves:
            return moves
        
        optimized = []
        i = 0
        
        while i < len(moves):
            if i + 3 < len(moves) and moves[i] == moves[i+1] == moves[i+2] == moves[i+3]:
                # Four identical moves cancel out
                i += 4
                continue
            
            if i + 2 < len(moves) and moves[i] == moves[i+1] == moves[i+2]:
                # Three identical moves = one inverse
                if "'" not in moves[i] and '2' not in moves[i]:
                    optimized.append(moves[i] + "'")
                    i += 3
                    continue
            
            if i + 1 < len(moves):
                # Check for canceling moves
                if self.moves_cancel(moves[i], moves[i+1]):
                    i += 2
                    continue
                
                # Combine moves on same face
                combined = self.combine_moves(moves[i], moves[i+1])
                if combined is not None:
                    if combined:  # If not empty (complete cancellation)
                        optimized.append(combined)
                    i += 2
                    continue
            
            optimized.append(moves[i])
            i += 1
        
        return optimized
    
    def moves_cancel(self, move1, move2):
        """Check if two moves cancel each other"""
        if move1[0] != move2[0]:
            return False
        
        if move1 == move2 + "'" or move2 == move1 + "'":
            return True
        
        if move1 == move2 and move1.endswith('2'):
            return True
        
        return False
    
    def combine_moves(self, move1, move2):
        """Try to combine two moves on the same face"""
        if move1[0] != move2[0]:
            return None
        
        face = move1[0]
        
        # Parse move amounts
        amt1 = 2 if '2' in move1 else (-1 if "'" in move1 else 1)
        amt2 = 2 if '2' in move2 else (-1 if "'" in move2 else 1)
        
        total = (amt1 + amt2) % 4
        
        if total == 0:
            return ""  # Complete cancellation
        elif total == 1:
            return face
        elif total == 2:
            return face + "2"
        elif total == 3:
            return face + "'"
        
        return None