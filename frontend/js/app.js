// frontend/js/app.js - Updated with proper error handling and backend integration

class RubiksCubeApp {
    constructor() {
        // FIXED: Changed port to 5001 to match backend
        this.apiUrl = 'http://localhost:5001/api';
        this.sessionId = 'session_' + Date.now();
        this.cube = new Cube();
        this.visualization = new CubeVisualization('cube3d');
        this.animationSpeed = 300;
        this.isAnimating = false;
        this.backendConnected = false;
        
        this.init();
    }
    
    async init() {
        console.log('🎯 Initializing Rubik\'s Cube Solver...');
        console.log(`📱 Session ID: ${this.sessionId}`);
        
        // Setup UI first
        this.setupEventListeners();
        this.updateVisualization();
        
        // Check backend connection
        await this.checkBackendConnection();
        
        // Initialize cube session
        if (this.backendConnected) {
            await this.createNewCube();
        } else {
            console.warn('⚠️ Backend not connected, running in offline mode');
            this.updateStatus('Offline Mode', 'warning');
        }
        
        console.log('✅ Application initialized successfully!');
    }
    
    async checkBackendConnection() {
        try {
            console.log('🔍 Checking backend connection...');
            const response = await fetch(`${this.apiUrl}/health`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('✅ Backend connected:', data.message);
                this.backendConnected = true;
                this.updateStatus('Connected', 'success');
            } else {
                throw new Error(`HTTP ${response.status}`);
            }
        } catch (error) {
            console.error('❌ Backend connection failed:', error);
            this.backendConnected = false;
            this.updateStatus('Backend Offline', 'error');
            this.showNotification('Backend server is not running on port 5001. Please start the backend server.', 'warning');
        }
    }
    
    setupEventListeners() {
        // Speed control
        const speedSlider = document.getElementById('speedSlider');
        const speedValue = document.getElementById('speedValue');
        
        if (speedSlider && speedValue) {
            speedSlider.addEventListener('input', (e) => {
                this.animationSpeed = parseInt(e.target.value);
                speedValue.textContent = `${this.animationSpeed}ms`;
            });
        }
        
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
            
            if (keyMap[e.key] && !e.ctrlKey && !e.altKey) {
                e.preventDefault();
                this.executeMove(keyMap[e.key]);
            }
        });
        
        // Add retry connection button
        this.addRetryButton();
    }
    
    addRetryButton() {
        const header = document.querySelector('.header');
        if (header && !document.getElementById('retryBtn')) {
            const retryBtn = document.createElement('button');
            retryBtn.id = 'retryBtn';
            retryBtn.className = 'btn btn-secondary';
            retryBtn.innerHTML = '🔄 Retry Connection';
            retryBtn.style.marginLeft = '10px';
            retryBtn.onclick = () => this.retryConnection();
            header.appendChild(retryBtn);
        }
    }
    
    async retryConnection() {
        this.updateStatus('Connecting...', 'warning');
        await this.checkBackendConnection();
        
        if (this.backendConnected) {
            await this.createNewCube();
        }
    }
    
    async createNewCube() {
        if (!this.backendConnected) {
            console.log('🔄 Creating cube in offline mode');
            this.cube.reset();
            this.updateVisualization();
            this.updateStatus('Offline - Ready', 'warning');
            return;
        }
        
        try {
            console.log('🎲 Creating new cube session...');
            const response = await fetch(`${this.apiUrl}/cube/new`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('✅ Cube session created:', data.message);
            
            this.cube.setState(data.state);
            this.updateVisualization();
            this.updateStatus('Ready', 'success');
            
            document.getElementById('statMoves').textContent = '0';
            document.getElementById('statTime').textContent = '0ms';
            document.getElementById('statAlgorithm').textContent = 'Layer-by-Layer';
            
        } catch (error) {
            console.error('❌ Error creating cube:', error);
            this.updateStatus('Error', 'error');
            this.showNotification(`Failed to create cube: ${error.message}`, 'error');
        }
    }
    
    async executeMove(move) {
        if (this.isAnimating) return;
        
        console.log(`🎯 Executing move: ${move}`);
        
        // Always update local cube first for immediate feedback
        try {
            this.cube.executeMove(move);
            this.updateVisualization();
        } catch (error) {
            console.error('❌ Invalid move:', move, error);
            this.showNotification(`Invalid move: ${move}`, 'error');
            return;
        }
        
        // Update backend if connected
        if (this.backendConnected) {
            try {
                const response = await fetch(`${this.apiUrl}/cube/move`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        session_id: this.sessionId,
                        move: move
                    })
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                
                const data = await response.json();
                if (data.success) {
                    // Sync with backend state
                    this.cube.setState(data.state);
                    this.updateVisualization();
                    document.getElementById('statMoves').textContent = data.move_count || this.cube.moveHistory.length;
                    
                    if (data.is_solved) {
                        this.updateStatus('Solved!', 'success');
                        this.showNotification('🎉 Cube solved!', 'success');
                    }
                } else {
                    throw new Error(data.error || 'Move failed');
                }
            } catch (error) {
                console.error('❌ Backend move error:', error);
                // Continue with local state, don't show error for every move
            }
        } else {
            // Update move count for offline mode
            document.getElementById('statMoves').textContent = this.cube.moveHistory.length;
            
            if (this.cube.isSolved()) {
                this.updateStatus('Solved!', 'success');
                this.showNotification('🎉 Cube solved!', 'success');
            }
        }
    }
    
    async scrambleCube() {
        if (this.isAnimating) return;
        
        console.log('🎲 Scrambling cube...');
        this.updateStatus('Scrambling...', 'warning');
        this.isAnimating = true;
        
        try {
            if (this.backendConnected) {
                // Use backend scramble
                const response = await fetch(`${this.apiUrl}/cube/scramble`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        session_id: this.sessionId,
                        num_moves: 25
                    })
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                
                const data = await response.json();
                console.log('✅ Backend scramble:', data.scramble_moves);
                
                // Set the scrambled state immediately
                this.cube.setState(data.state);
                this.updateVisualization();
                this.updateStatus('Scrambled', 'normal');
                
                // Display scramble sequence
                this.displayScramble(data.scramble_moves);
                
            } else {
                // Offline scramble
                console.log('🔄 Offline scramble...');
                this.cube.reset(); // Start from solved
                
                const moves = ['U', "U'", 'U2', 'D', "D'", 'D2', 'R', "R'", 'R2', 
                              'L', "L'", 'L2', 'F', "F'", 'F2', 'B', "B'", 'B2'];
                const scrambleMoves = [];
                
                for (let i = 0; i < 25; i++) {
                    const move = moves[Math.floor(Math.random() * moves.length)];
                    scrambleMoves.push(move);
                    this.cube.executeMove(move);
                    this.updateVisualization();
                    await this.sleep(this.animationSpeed / 3);
                }
                
                this.updateStatus('Scrambled (Offline)', 'warning');
                this.displayScramble(scrambleMoves);
            }
            
        } catch (error) {
            console.error('❌ Scramble error:', error);
            this.updateStatus('Scramble Failed', 'error');
            this.showNotification(`Scramble failed: ${error.message}`, 'error');
        } finally {
            this.isAnimating = false;
        }
    }
    
    async resetCube() {
        if (this.isAnimating) return;
        
        console.log('🔄 Resetting cube...');
        
        if (this.backendConnected) {
            try {
                const response = await fetch(`${this.apiUrl}/cube/reset`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: this.sessionId })
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                
                const data = await response.json();
                console.log('✅ Cube reset:', data.message);
                
                this.cube.setState(data.state);
                
            } catch (error) {
                console.error('❌ Reset error:', error);
                this.showNotification(`Reset failed: ${error.message}`, 'error');
                // Fall back to local reset
                this.cube.reset();
            }
        } else {
            this.cube.reset();
        }
        
        this.cube.moveHistory = [];
        this.updateVisualization();
        this.updateStatus('Ready', 'success');
        
        // Reset statistics
        document.getElementById('statMoves').textContent = '0';
        document.getElementById('statTime').textContent = '0ms';
        document.getElementById('solutionContent').innerHTML = '<p class="placeholder">Execute a solve to see the solution steps...</p>';
        
        console.log('✅ Cube reset complete');
    }
    
    async solveCube() {
        if (this.isAnimating) return;
        
        if (!this.backendConnected) {
            this.showNotification('Backend connection required for solving', 'warning');
            return;
        }
        
        console.log('🚀 Starting cube solve...');
        this.updateStatus('Solving...', 'warning');
        this.isAnimating = true;
        
        const cubeElement = document.getElementById('cube3d');
        cubeElement.classList.add('solving');
        
        try {
            // Get the current state before solving
            const initialState = JSON.parse(JSON.stringify(this.cube.state));
            
            const response = await fetch(`${this.apiUrl}/cube/solve`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ session_id: this.sessionId })
            });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }
            
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'Solve failed');
            }
            
            console.log('✅ Solution found:', data.solution);
            console.log(`📊 Stats: ${data.move_count} moves, ${Math.round(data.solve_time)}ms`);
            
            // Display solution info immediately
            this.displaySolution(data);
            
            // Update statistics
            document.getElementById('statMoves').textContent = data.move_count;
            document.getElementById('statTime').textContent = `${Math.round(data.solve_time)}ms`;
            document.getElementById('statAlgorithm').textContent = data.algorithm || 'Layer-by-Layer';
            
            // Animate the solution if there are moves
            if (data.solution && data.solution.length > 0) {
                this.updateStatus('Animating...', 'warning');
                
                // Reset to initial state for animation
                this.cube.setState(initialState);
                this.updateVisualization();
                
                // Wait a moment before starting animation
                await this.sleep(500);
                
                // Animate each move
                for (let i = 0; i < data.solution.length; i++) {
                    const move = data.solution[i];
                    
                    // Execute move
                    this.cube.executeMove(move);
                    this.updateVisualization();
                    
                    // Highlight current move in solution display
                    this.highlightCurrentMove(i);
                    
                    // Update progress
                    this.updateStatus(`Move ${i + 1}/${data.solution.length}`, 'warning');
                    
                    // Wait for animation
                    await this.sleep(this.animationSpeed);
                }
                
                // Clear move highlighting
                this.clearMoveHighlight();
            }
            
            // Verify final state matches
            if (data.final_state) {
                this.cube.setState(data.final_state);
                this.updateVisualization();
            }
            
            if (data.is_solved || this.cube.isSolved()) {
                this.updateStatus('Solved!', 'success');
                this.showNotification('🎉 Cube solved successfully!', 'success');
                
                // Add celebration effect
                this.celebrateSolution();
            } else {
                this.updateStatus('Incomplete', 'warning');
                this.showNotification('⚠️ Solution may be incomplete. Try again.', 'warning');
            }
            
        } catch (error) {
            console.error('❌ Solve error:', error);
            this.updateStatus('Solve Failed', 'error');
            this.showNotification(`Solve failed: ${error.message}`, 'error');
            
            // Log additional error details for debugging
            if (error.message.includes('traceback')) {
                console.error('Backend traceback available in response');
            }
            
        } finally {
            this.isAnimating = false;
            cubeElement.classList.remove('solving');
        }
    }
    
    highlightCurrentMove(index) {
        // Remove all highlights
        const moveTags = document.querySelectorAll('.move-tag');
        moveTags.forEach(tag => tag.classList.remove('current-move'));
        
        // Add highlight to current move
        if (moveTags[index]) {
            moveTags[index].classList.add('current-move');
            moveTags[index].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }
    
    clearMoveHighlight() {
        const moveTags = document.querySelectorAll('.move-tag');
        moveTags.forEach(tag => tag.classList.remove('current-move'));
    }
    
    celebrateSolution() {
        const cubeElement = document.getElementById('cube3d');
        cubeElement.classList.add('celebrate');
        
        setTimeout(() => {
            cubeElement.classList.remove('celebrate');
        }, 2000);
    }
    
    displayScramble(scrambleMoves) {
        const content = document.getElementById('solutionContent');
        content.innerHTML = `
            <div class="solution-phase">
                <h4>Scramble Sequence (${scrambleMoves.length} moves)</h4>
                <div class="moves-list">
                    ${scrambleMoves.map(m => `<span class="move-tag">${m}</span>`).join('')}
                </div>
            </div>
        `;
    }
    
    displaySolution(data) {
        const content = document.getElementById('solutionContent');
        
        let html = `
            <div class="solution-summary">
                <p><strong>Algorithm:</strong> ${data.algorithm || 'Layer-by-Layer'}</p>
                <p><strong>Total Moves:</strong> ${data.move_count}</p>
                <p><strong>Solve Time:</strong> ${Math.round(data.solve_time)}ms</p>
            </div>
        `;
        
        if (data.solution && data.solution.length > 0) {
            html += `
                <div class="solution-phase">
                    <h4>Solution (${data.solution.length} moves)</h4>
                    <div class="moves-list">
                        ${data.solution.map(m => `<span class="move-tag">${m}</span>`).join('')}
                    </div>
                </div>
            `;
        }
        
        content.innerHTML = html;
    }
    
    updateVisualization() {
        if (this.visualization) {
            this.visualization.update(this.cube.state);
        }
    }
    
    updateStatus(text, type = 'normal') {
        const element = document.getElementById('statStatus');
        if (element) {
            element.textContent = text;
            
            const colors = {
                'success': '#06d6a0',
                'warning': '#ffd166',
                'error': '#ef476f',
                'normal': '#06d6a0'
            };
            
            element.style.color = colors[type] || colors.normal;
        }
        
        console.log(`📊 Status: ${text}`);
    }
    
    showNotification(message, type = 'info') {
        // Create notification element if it doesn't exist
        let notification = document.getElementById('notification');
        if (!notification) {
            notification = document.createElement('div');
            notification.id = 'notification';
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 5px;
                color: white;
                font-weight: bold;
                z-index: 1000;
                max-width: 300px;
                opacity: 0;
                transition: opacity 0.3s;
            `;
            document.body.appendChild(notification);
        }
        
        // Set colors based on type
        const colors = {
            'success': '#06d6a0',
            'warning': '#ffd166',
            'error': '#ef476f',
            'info': '#118ab2'
        };
        
        notification.style.backgroundColor = colors[type] || colors.info;
        notification.textContent = message;
        notification.style.opacity = '1';
        
        // Auto hide after 3 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
        }, 3000);
        
        console.log(`🔔 ${type.toUpperCase()}: ${message}`);
    }
    
    rotateView(axis) {
        if (this.visualization) {
            this.visualization.rotate(axis);
        }
    }
    
    resetView() {
        if (this.visualization) {
            this.visualization.resetRotation();
        }
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎯 Starting Rubik\'s Cube Solver Application...');
    window.app = new RubiksCubeApp();
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    console.log('👋 Application shutting down...');
});