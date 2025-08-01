// frontend/js/solver.js

class Solver {
    constructor() {
        this.algorithms = {
            'layer_by_layer': 'Layer by Layer (CFOP)',
            'kociemba': 'Kociemba Two-Phase',
            'beginner': 'Beginner Method'
        };
    }
    
    getAlgorithmName(id) {
        return this.algorithms[id] || 'Unknown';
    }
    
    // Client-side solving logic could be added here
    // Currently, all solving is done on the backend
}