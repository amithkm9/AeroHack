// frontend/js/app.js

class RubiksCubeApp {
    constructor() {
        this.apiUrl = 'http://localhost:5001/api';
        this.sessionId = this.generateSessionId();
        this.cube = new Cube();
        this.visualization = new CubeVisualization('cube3d');
        this.solver = new Solver();
        this.selectedAlgorithm = 'layer_by_layer';
        this.animationSpeed = 300;
        this.isAnimating = false;
        
        this.init();
    }
    
    async init() {
        // Initialize cube on backend
        await this.createNewCube();
        
        // Load available algorithms
        await this.loadAlgorithms();
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Initial visualization
        this.updateVisualization();
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    setupEventListeners() {
        // Speed control
        const speedSlider = document.getElementById('speedSlider');
        const speedValue = document.getElementById('speedValue');
        
        speedSlider.addEventListener('input', (e) => {
            this.animationSpeed = parseInt(e.target.value);
            speedValue.textContent = `${this.animationSpeed}ms`;
        });
        
        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            if (this.isAnimating) return;
            
            const keyMap = {
                'u': 'U', 'U': "U'",
                'd': 'D', 'D': "D'",
                'r': 'R', 'R': "R'",
                'l': 'L', 'L': "L'",
                'f': 'F', 'F': "F'",
                'b': 'B', 'B': "B'"
            };
            
            if (keyMap[e.key]) {
                this.executeMove(keyMap[e.key]);
            }
        });
    }
    
    async createNewCube() {
        try {
            const response = await fetch(`${this.apiUrl}/cube/new`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId })
            });
            
            const data = await response.json();
            this.cube.setState(data.state);
            this.updateStatus('Ready');
        } catch (error) {
            console.error('Error creating cube:', error);
            this.updateStatus('Error', 'error');
        }
    }
    
    async loadAlgorithms() {
        try {
            const response = await fetch(`${this.apiUrl}/algorithms`);
            const data = await response.json();
            
            const container = document.getElementById('algorithmCards');
            container.innerHTML = '';
            
            data.algorithms.forEach(algo => {
                const card = document.createElement('div');
                card.className = 'algorithm-card';
                card.dataset.algorithmId = algo.id;
                
                if (algo.id === this.selectedAlgorithm) {
                    card.classList.add('selected');
                }
                
                card.innerHTML = `
                    <h4>${algo.name}</h4>
                    <p>${algo.description}</p>
                    <div class="algorithm-meta">
                        <span class="difficulty ${algo.difficulty.toLowerCase()}">${algo.difficulty}</span>
                        <span>~${algo.average_moves} moves</span>
                    </div>
                `;
                
                card.addEventListener('click', () => {
                    document.querySelectorAll('.algorithm-card').forEach(c => c.classList.remove('selected'));
                    card.classList.add('selected');
                    this.selectedAlgorithm = algo.id;
                    document.getElementById('statAlgorithm').textContent = algo.name;
                });
                
                container.appendChild(card);
            });
            
            // Set initial algorithm display
            const selectedAlgo = data.algorithms.find(a => a.id === this.selectedAlgorithm);
            if (selectedAlgo) {
                document.getElementById('statAlgorithm').textContent = selectedAlgo.name;
            }
        } catch (error) {
            console.error('Error loading algorithms:', error);
        }
    }
    
    async executeMove(move) {
        if (this.isAnimating) return;
        
        try {
            const response = await fetch(`${this.apiUrl}/cube/move`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    move: move
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.cube.setState(data.state);
                this.updateVisualization();
                this.updateMoveCount();
                
                if (data.is_solved) {
                    this.updateStatus('Solved!', 'success');
                }
            }
        } catch (error) {
            console.error('Error executing move:', error);
        }
    }
    
    async scrambleCube() {
        if (this.isAnimating) return;
        
        this.updateStatus('Scrambling...', 'warning');
        
        try {
            const response = await fetch(`${this.apiUrl}/cube/scramble`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    num_moves: 25
                })
            });
            
            const data = await response.json();
            
            // Animate scramble
            this.isAnimating = true;
            for (const move of data.scramble_moves) {
                this.cube.executeMove(move);
                this.updateVisualization();
                await this.sleep(this.animationSpeed / 2);
            }
            this.isAnimating = false;
            
            this.cube.setState(data.state);
            this.updateVisualization();
            this.updateStatus('Scrambled', 'warning');
            this.updateMoveCount();
            
            // Display scramble in solution panel
            this.displayScramble(data.scramble_moves);
        } catch (error) {
            console.error('Error scrambling cube:', error);
            this.updateStatus('Error', 'error');
            this.isAnimating = false;
        }
    }
    
    async resetCube() {
        if (this.isAnimating) return;
        
        try {
            const response = await fetch(`${this.apiUrl}/cube/reset`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId })
            });
            
            const data = await response.json();
            this.cube.setState(data.state);
            this.updateVisualization();
            this.updateStatus('Ready');
            this.resetStats();
            this.clearSolutionDisplay();
        } catch (error) {
            console.error('Error resetting cube:', error);
        }
    }
    
    async solveCube() {
        if (this.isAnimating) return;
        
        this.updateStatus('Solving...', 'warning');
        this.isAnimating = true;
        document.getElementById('cube3d').classList.add('solving');
        
        try {
            const startTime = performance.now();
            
            const response = await fetch(`${this.apiUrl}/cube/solve`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    method: this.selectedAlgorithm
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Display solution breakdown
                this.displaySolution(data);
                
                // Animate solution
                for (const move of data.solution) {
                    this.cube.executeMove(move);
                    this.updateVisualization();
                    await this.sleep(this.animationSpeed);
                }
                
                // Update final state
                this.cube.setState(data.final_state);
                this.updateVisualization();
                
                // Update stats
                document.getElementById('statMoves').textContent = data.move_count;
                document.getElementById('statTime').textContent = `${Math.round(data.solve_time)}ms`;
                this.updateStatus('Solved!', 'success');
            } else {
                this.updateStatus('Solve Failed', 'error');
                console.error('Solve error:', data.error);
            }
        } catch (error) {
            console.error('Error solving cube:', error);
            this.updateStatus('Error', 'error');
        } finally {
            this.isAnimating = false;
            document.getElementById('cube3d').classList.remove('solving');
        }
    }
    
    updateVisualization() {
        this.visualization.update(this.cube.state);
    }
    
    updateStatus(status, type = 'normal') {
        const statusElement = document.getElementById('statStatus');
        statusElement.textContent = status;
        statusElement.className = 'stat-value';
        
        if (type === 'success') {
            statusElement.style.color = 'var(--success-color)';
        } else if (type === 'warning') {
            statusElement.style.color = 'var(--warning-color)';
        } else if (type === 'error') {
            statusElement.style.color = 'var(--error-color)';
        } else {
            statusElement.style.color = 'var(--primary-color)';
        }
    }
    
    updateMoveCount() {
        document.getElementById('statMoves').textContent = this.cube.moveHistory.length;
    }
    
    resetStats() {
        document.getElementById('statMoves').textContent = '0';
        document.getElementById('statTime').textContent = '0ms';
    }
    
    displayScramble(moves) {
        const container = document.getElementById('solutionContent');
        container.innerHTML = `
            <div class="solution-phase">
                <h4>Scramble Sequence</h4>
                <div class="moves-list">
                    ${moves.map(move => `<span class="move-tag">${move}</span>`).join('')}
                </div>
            </div>
        `;
    }
    
    displaySolution(data) {
        const container = document.getElementById('solutionContent');
        container.innerHTML = '';
        
        // Add summary
        const summary = document.createElement('div');
        summary.className = 'solution-summary';
        summary.innerHTML = `
            <p><strong>Algorithm:</strong> ${this.selectedAlgorithm.replace(/_/g, ' ').toUpperCase()}</p>
            <p><strong>Total Moves:</strong> ${data.move_count}</p>
            <p><strong>Solve Time:</strong> ${Math.round(data.solve_time)}ms</p>
        `;
        container.appendChild(summary);
        
        // Add phases
        for (const [phase, moves] of Object.entries(data.phases)) {
            if (moves.length === 0) continue;
            
            const phaseDiv = document.createElement('div');
            phaseDiv.className = 'solution-phase';
            phaseDiv.innerHTML = `
                <h4>${phase.replace(/_/g, ' ').toUpperCase()} (${moves.length} moves)</h4>
                <div class="moves-list">
                    ${moves.map(move => `<span class="move-tag">${move}</span>`).join('')}
                </div>
            `;
            container.appendChild(phaseDiv);
        }
    }
    
    clearSolutionDisplay() {
        document.getElementById('solutionContent').innerHTML = `
            <p class="placeholder">Execute a solve to see the solution steps...</p>
        `;
    }
    
    rotateView(axis) {
        this.visualization.rotate(axis);
    }
    
    resetView() {
        this.visualization.resetRotation();
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new RubiksCubeApp();
});