from typing import Dict

class BeginnerMethodSolver:
    """Beginner-friendly solving method"""
    
    def __init__(self, cube):
        self.cube = cube
        self.solution = []
    
    def solve(self) -> Dict:
        self.solution = []
        
        # Simple beginner algorithms
        algorithms = [
            ['F', 'R', 'U', 'R\'', 'F\''],  # Cross
            ['R', 'U', 'R\'', 'U\''] * 3,    # Corners
            ['U', 'R', 'U\'', 'R\'', 'F\'', 'U\'', 'F'],  # Middle
            ['F', 'R', 'U', 'R\'', 'U\'', 'F\'']  # Top
        ]
        
        phases = {}
        phase_names = ['cross', 'corners', 'middle', 'top']
        
        for i, (name, algo) in enumerate(zip(phase_names, algorithms)):
            start = len(self.solution)
            for move in algo:
                self.cube.execute_move(move)
                self.solution.append(move)
            phases[name] = self.solution[start:]
        
        return {
            'solution': self.solution,
            'phases': phases
        }