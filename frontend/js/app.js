// frontend/js/app.js

class RubiksCubeApp {
    constructor() {
        this.apiUrl = 'http://localhost:5000/api';
        this.sessionId = 'session_' + Date.now();
        this.cube = new Cube();
        this.visualization = new CubeVisualization('cube3d');
        this.animationSpeed = 300;
        this.isAnimating = false;
        
        this.init();
    }
    
    async init() {
        await this.createNewCube();
        this.setupEventListeners();
        this.updateVisualization();
    }
    
    setupEventListeners() {
        // Speed control
        const speedSlider = document.getElementById('speedSlider');
        speedSlider.addEventListener('input', (e) => {
            this.animationSpeed = parseInt(e.target.value);
            document.getElementById('speedValue').textContent = `${this.animationSpeed}ms`;
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
            console.error('Error:', error);
            this.updateStatus('Error connecting to server', 'error');
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
                document.getElementById('statMoves').textContent = this.cube.moveHistory.length;
                
                if (data.is_solved) {
                    this.updateStatus('Solved!', 'success');
                }
            }
        } catch (error) {
            console.error('Error:', error);
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
            this.updateStatus('Scrambled');
            
            // Display scramble
            document.getElementById('solutionContent').innerHTML = `
                <div class="solution-phase">
                    <h4>Scramble Sequence</h4>
                    <div class="moves-list">
                        ${data.scramble_moves.map(m => `<span class="move-tag">${m}</span>`).join('')}
                    </div>
                </div>
            `;
        } catch (error) {
            console.error('Error:', error);
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
            this.cube.moveHistory = [];
            this.updateVisualization();
            this.updateStatus('Ready');
            document.getElementById('statMoves').textContent = '0';
            document.getElementById('statTime').textContent = '0ms';
            document.getElementById('solutionContent').innerHTML = '<p class="placeholder">Execute a solve to see the solution steps...</p>';
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    async solveCube() {
        if (this.isAnimating) return;
        
        this.updateStatus('Solving...', 'warning');
        this.isAnimating = true;
        document.getElementById('cube3d').classList.add('solving');
        
        try {
            const response = await fetch(`${this.apiUrl}/cube/solve`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Display solution
                this.displaySolution(data);
                
                // Animate solution
                for (const move of data.solution) {
                    this.cube.executeMove(move);
                    this.updateVisualization();
                    await this.sleep(this.animationSpeed);
                }
                
                this.cube.setState(data.final_state);
                this.updateVisualization();
                
                document.getElementById('statMoves').textContent = data.move_count;
                document.getElementById('statTime').textContent = `${Math.round(data.solve_time)}ms`;
                this.updateStatus('Solved!', 'success');
            }
        } catch (error) {
            console.error('Error:', error);
            this.updateStatus('Error', 'error');
        } finally {
            this.isAnimating = false;
            document.getElementById('cube3d').classList.remove('solving');
        }
    }
    
    displaySolution(data) {
        const content = document.getElementById('solutionContent');
        content.innerHTML = `
            <div class="solution-summary">
                <p><strong>Algorithm:</strong> Kociemba Two-Phase</p>
                <p><strong>Total Moves:</strong> ${data.move_count}</p>
                <p><strong>Solve Time:</strong> ${Math.round(data.solve_time)}ms</p>
            </div>
        `;
        
        if (data.phases.phase1 && data.phases.phase1.length > 0) {
            content.innerHTML += `
                <div class="solution-phase">
                    <h4>Phase 1: Orientation (${data.phases.phase1.length} moves)</h4>
                    <div class="moves-list">
                        ${data.phases.phase1.map(m => `<span class="move-tag">${m}</span>`).join('')}
                    </div>
                </div>
            `;
        }
        
        if (data.phases.phase2 && data.phases.phase2.length > 0) {
            content.innerHTML += `
                <div class="solution-phase">
                    <h4>Phase 2: Permutation (${data.phases.phase2.length} moves)</h4>
                    <div class="moves-list">
                        ${data.phases.phase2.map(m => `<span class="move-tag">${m}</span>`).join('')}
                    </div>
                </div>
            `;
        }
    }
    
    updateVisualization() {
        this.visualization.update(this.cube.state);
    }
    
    updateStatus(text, type = 'normal') {
        const element = document.getElementById('statStatus');
        element.textContent = text;
        
        const colors = {
            'success': '#06d6a0',
            'warning': '#ffd166',
            'error': '#ef476f',
            'normal': '#06d6a0'
        };
        
        element.style.color = colors[type] || colors.normal;
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

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.app = new RubiksCubeApp();
});