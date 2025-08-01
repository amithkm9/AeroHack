# backend/solvers/layer_by_layer.py
from typing import List, Dict, Tuple, Optional

class LayerByLayerSolver:
    """
    Advanced Layer-by-Layer (CFOP) solver
    """
    
    def __init__(self, cube):
        self.cube = cube
        self.solution = []
        
    def solve(self) -> Dict:
        """Main solving method"""
        self.solution = []
        phases = {}
        
        if self.cube.is_solved():
            return {
                'solution': [],
                'phases': {},
                'already_solved': True
            }
        
        # Cross
        start = len(self.solution)
        self.solve_cross()
        phases['cross'] = self.solution[start:]
        
        # F2L (First Two Layers)
        start = len(self.solution)
        self.solve_f2l()
        phases['f2l'] = self.solution[start:]
        
        # OLL (Orientation of Last Layer)
        start = len(self.solution)
        self.solve_oll()
        phases['oll'] = self.solution[start:]
        
        # PLL (Permutation of Last Layer)
        start = len(self.solution)
        self.solve_pll()
        phases['pll'] = self.solution[start:]
        
        return {
            'solution': self.solution,
            'phases': phases,
            'already_solved': False
        }
    
    def apply_algorithm(self, moves: List[str]):
        """Apply an algorithm and add to solution"""
        for move in moves:
            self.cube.execute_move(move)
            self.solution.append(move)
    
    def solve_cross(self):
        """Solve white cross on top"""
        # Target edges for white cross
        edges = [
            (['W', 'G'], ('U', 7), ('F', 1)),
            (['W', 'R'], ('U', 5), ('R', 1)),
            (['W', 'B'], ('U', 1), ('B', 1)),
            (['W', 'O'], ('U', 3), ('L', 1))
        ]
        
        for colors, u_pos, side_pos in edges:
            self._solve_cross_edge(colors, u_pos, side_pos)
    
    def _solve_cross_edge(self, colors: List[str], u_pos: Tuple[str, int], side_pos: Tuple[str, int]):
        """Position a single cross edge"""
        for _ in range(20):  # Max attempts
            edge = self.cube.find_piece(colors)
            if not edge:
                break
                
            # Check if correctly positioned
            if edge[0] == ('U', u_pos[1]) and edge[1] == side_pos:
                if self.cube.state['U'][u_pos[1]] == 'W':
                    break
            
            # Get edge to bottom layer if not there
            if edge[0][0] == 'U' or edge[1][0] == 'U':
                # Edge in top layer, move to bottom
                for pos in edge:
                    if pos[0] != 'U' and pos[1] == 1:
                        self.apply_algorithm([pos[0], pos[0]])
                        break
            elif any(pos[1] in [3, 5] for pos in edge):
                # Edge in middle layer
                for pos in edge:
                    if pos[1] == 3:
                        self.apply_algorithm([pos[0], 'D', pos[0] + "'", "D'"])
                        break
                    elif pos[1] == 5:
                        self.apply_algorithm([pos[0] + "'", "D'", pos[0], 'D'])
                        break
            
            # Now edge should be in bottom layer
            edge = self.cube.find_piece(colors)
            if edge and any(pos[0] == 'D' for pos in edge):
                # Align with target position
                target_face = side_pos[0]
                current_face = next(pos[0] for pos in edge if pos[0] != 'D')
                
                # Calculate D moves needed
                faces = ['F', 'R', 'B', 'L']
                if current_face in faces and target_face in faces:
                    current_idx = faces.index(current_face)
                    target_idx = faces.index(target_face)
                    d_moves = (target_idx - current_idx) % 4
                    
                    for _ in range(d_moves):
                        self.apply_algorithm(['D'])
                
                # Insert edge
                self.apply_algorithm([target_face, target_face])
    
    def solve_f2l(self):
        """Solve First Two Layers"""
        # F2L pairs
        pairs = [
            (['W', 'G', 'R'], ['G', 'R']),  # Front-Right
            (['W', 'R', 'B'], ['R', 'B']),  # Right-Back
            (['W', 'B', 'O'], ['B', 'O']),  # Back-Left
            (['W', 'O', 'G'], ['O', 'G'])   # Left-Front
        ]
        
        for corner_colors, edge_colors in pairs:
            self._solve_f2l_pair(corner_colors, edge_colors)
    
    def _solve_f2l_pair(self, corner_colors: List[str], edge_colors: List[str]):
        """Solve one F2L pair"""
        # This is a simplified F2L - full implementation would have 41 cases
        
        # First, get corner to bottom layer
        for _ in range(10):
            corner = self.cube.find_piece(corner_colors)
            if corner and any(pos[0] == 'U' for pos in corner):
                # Corner in top layer - take it out
                for pos in corner:
                    if pos[0] != 'U':
                        face = pos[0]
                        if pos[1] in [0, 2]:
                            self.apply_algorithm([face, "D'", face + "'"])
                            break
            else:
                break
        
        # Get edge to top layer if in middle
        edge = self.cube.find_piece(edge_colors)
        if edge and all(pos[1] in [3, 5] for pos in edge):
            # Edge in middle layer - take it out
            face = edge[0][0]
            self.apply_algorithm([face, 'U', face + "'", "U'", face + "'", "U'", face])
        
        # Now pair and insert (simplified - just using basic insertion)
        # In full implementation, this would recognize all 41 F2L cases
        corner = self.cube.find_piece(corner_colors)
        edge = self.cube.find_piece(edge_colors)
        
        if corner and edge:
            # Basic pairing and insertion
            # This is greatly simplified - real F2L would be much more sophisticated
            self.apply_algorithm(['U', 'R', "U'", "R'", "U'", "F'", 'U', 'F'])
    
    def solve_oll(self):
        """Solve OLL (Orient Last Layer)"""
        # Count yellow stickers on bottom
        yellow_count = sum(1 for i in range(9) if self.cube.state['D'][i] == 'Y')
        
        if yellow_count == 9:
            return  # Already oriented
        
        # OLL algorithms (simplified - full OLL has 57 cases)
        # Here we'll just use a few basic patterns
        
        # Dot pattern
        if yellow_count == 1:
            self.apply_algorithm(['F', 'R', 'U', "R'", "U'", "F'", 'f', 'R', 'U', "R'", "U'", "f'"])
        
        # Line pattern
        elif self.cube.state['D'][1] == 'Y' and self.cube.state['D'][7] == 'Y':
            self.apply_algorithm(['F', 'R', 'U', "R'", "U'", "F'"])
        
        # L pattern
        elif yellow_count == 3:
            # Orient L shape correctly
            for _ in range(4):
                if (self.cube.state['D'][1] == 'Y' and 
                    self.cube.state['D'][3] == 'Y' and 
                    self.cube.state['D'][4] == 'Y'):
                    break
                self.apply_algorithm(['U'])
            
            self.apply_algorithm(['F', 'U', 'R', "U'", "R'", "F'"])
        
        # If still not solved, apply sune repeatedly
        for _ in range(6):
            if all(self.cube.state['D'][i] == 'Y' for i in range(9)):
                break
            self.apply_algorithm(['R', 'U', "R'", 'U', 'R', 'U2', "R'"])
    
    def solve_pll(self):
        """Solve PLL (Permute Last Layer)"""
        # This is simplified - full PLL has 21 cases
        
        # First solve corners
        self._solve_pll_corners()
        
        # Then solve edges
        self._solve_pll_edges()
    
    def _solve_pll_corners(self):
        """Position corners correctly"""
        # Check how many corners are in correct position
        correct_corners = self._count_correct_corners()
        
        if correct_corners == 4:
            return  # All corners correct
        
        # A-perm algorithm for corner swap
        if correct_corners == 1:
            # Position the correct corner in back-left
            for _ in range(4):
                if self._is_corner_correct(2):  # Back-left position
                    break
                self.apply_algorithm(['U'])
        
        # Apply corner permutation algorithm
        self.apply_algorithm(['U', 'R', "U'", "L'", 'U', "R'", "U'", 'L'])
    
    def _solve_pll_edges(self):
        """Position edges correctly"""
        # Check edge configuration
        correct_edges = self._count_correct_edges()
        
        if correct_edges == 4:
            return  # All edges correct
        
        # U-perm for edge cycling
        if correct_edges == 0:
            self.apply_algorithm(['R2', 'U', 'R', 'U', "R'", "U'", "R'", "U'", "R'", 'U', "R'"])
        
        # H-perm for opposite edge swap
        elif correct_edges == 0:
            self.apply_algorithm(['R2', 'U2', 'R', 'U2', 'R2', 'U2', 'R2', 'U2', 'R', 'U2', 'R2'])
    
    def _count_correct_corners(self) -> int:
        """Count corners in correct position"""
        count = 0
        corners = [
            ([('D', 0), ('F', 6), ('L', 6)], ['Y', 'G', 'O']),
            ([('D', 2), ('F', 8), ('R', 6)], ['Y', 'G', 'R']),
            ([('D', 8), ('B', 8), ('R', 8)], ['Y', 'B', 'R']),
            ([('D', 6), ('B', 6), ('L', 8)], ['Y', 'B', 'O'])
        ]
        
        for positions, target_colors in corners:
            current_colors = set(self.cube.get_piece_at(positions))
            if current_colors == set(target_colors):
                count += 1
        
        return count
    
    def _count_correct_edges(self) -> int:
        """Count edges in correct position"""
        count = 0
        edges = [
            ([('D', 1), ('F', 7)], ['Y', 'G']),
            ([('D', 5), ('R', 7)], ['Y', 'R']),
            ([('D', 7), ('B', 7)], ['Y', 'B']),
            ([('D', 3), ('L', 7)], ['Y', 'O'])
        ]
        
        for positions, target_colors in edges:
            current = self.cube.get_piece_at(positions)
            if current == target_colors:
                count += 1
        
        return count
    
    def _is_corner_correct(self, index: int) -> bool:
        """Check if specific corner is in correct position"""
        corners = [
            ([('D', 0), ('F', 6), ('L', 6)], ['Y', 'G', 'O']),
            ([('D', 2), ('F', 8), ('R', 6)], ['Y', 'G', 'R']),
            ([('D', 8), ('B', 8), ('R', 8)], ['Y', 'B', 'R']),
            ([('D', 6), ('B', 6), ('L', 8)], ['Y', 'B', 'O'])
        ]
        
        positions, target_colors = corners[index]
        current_colors = set(self.cube.get_piece_at(positions))
        return current_colors == set(target_colors)