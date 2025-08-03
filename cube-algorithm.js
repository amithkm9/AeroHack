// ========== CUBE REPRESENTATION ==========
class Cube {
    constructor() {
        this.reset();
    }

    reset() {
        this.state = {
            'U': ['W','W','W','W','W','W','W','W','W'],
            'D': ['Y','Y','Y','Y','Y','Y','Y','Y','Y'],
            'F': ['G','G','G','G','G','G','G','G','G'],
            'B': ['B','B','B','B','B','B','B','B','B'],
            'R': ['R','R','R','R','R','R','R','R','R'],
            'L': ['O','O','O','O','O','O','O','O','O']
        };
    }

    copy() {
        const newCube = new Cube();
        newCube.state = JSON.parse(JSON.stringify(this.state));
        return newCube;
    }

    executeMove(move) {
        const face = move[0];
        const modifier = move.slice(1);
        
        let rotations = 1;
        if (modifier === "'") rotations = 3;
        else if (modifier === "2") rotations = 2;
        
        for (let i = 0; i < rotations; i++) {
            switch(face) {
                case 'U': this.moveU(); break;
                case 'D': this.moveD(); break;
                case 'R': this.moveR(); break;
                case 'L': this.moveL(); break;
                case 'F': this.moveF(); break;
                case 'B': this.moveB(); break;
            }
        }
    }

    rotateFace(face) {
        const f = this.state[face];
        const temp = [...f];
        f[0] = temp[6]; f[1] = temp[3]; f[2] = temp[0];
        f[3] = temp[7]; f[4] = temp[4]; f[5] = temp[1];
        f[6] = temp[8]; f[7] = temp[5]; f[8] = temp[2];
    }

    moveU() {
        this.rotateFace('U');
        const temp = [this.state['F'][0], this.state['F'][1], this.state['F'][2]];
        this.state['F'][0] = this.state['R'][0];
        this.state['F'][1] = this.state['R'][1];
        this.state['F'][2] = this.state['R'][2];
        this.state['R'][0] = this.state['B'][0];
        this.state['R'][1] = this.state['B'][1];
        this.state['R'][2] = this.state['B'][2];
        this.state['B'][0] = this.state['L'][0];
        this.state['B'][1] = this.state['L'][1];
        this.state['B'][2] = this.state['L'][2];
        this.state['L'][0] = temp[0];
        this.state['L'][1] = temp[1];
        this.state['L'][2] = temp[2];
    }

    moveD() {
        this.rotateFace('D');
        const temp = [this.state['F'][6], this.state['F'][7], this.state['F'][8]];
        this.state['F'][6] = this.state['L'][6];
        this.state['F'][7] = this.state['L'][7];
        this.state['F'][8] = this.state['L'][8];
        this.state['L'][6] = this.state['B'][6];
        this.state['L'][7] = this.state['B'][7];
        this.state['L'][8] = this.state['B'][8];
        this.state['B'][6] = this.state['R'][6];
        this.state['B'][7] = this.state['R'][7];
        this.state['B'][8] = this.state['R'][8];
        this.state['R'][6] = temp[0];
        this.state['R'][7] = temp[1];
        this.state['R'][8] = temp[2];
    }

    moveR() {
        this.rotateFace('R');
        const temp = [this.state['F'][2], this.state['F'][5], this.state['F'][8]];
        this.state['F'][2] = this.state['D'][2];
        this.state['F'][5] = this.state['D'][5];
        this.state['F'][8] = this.state['D'][8];
        this.state['D'][2] = this.state['B'][6];
        this.state['D'][5] = this.state['B'][3];
        this.state['D'][8] = this.state['B'][0];
        this.state['B'][0] = this.state['U'][8];
        this.state['B'][3] = this.state['U'][5];
        this.state['B'][6] = this.state['U'][2];
        this.state['U'][2] = temp[0];
        this.state['U'][5] = temp[1];
        this.state['U'][8] = temp[2];
    }

    moveL() {
        this.rotateFace('L');
        const temp = [this.state['F'][0], this.state['F'][3], this.state['F'][6]];
        this.state['F'][0] = this.state['U'][0];
        this.state['F'][3] = this.state['U'][3];
        this.state['F'][6] = this.state['U'][6];
        this.state['U'][0] = this.state['B'][8];
        this.state['U'][3] = this.state['B'][5];
        this.state['U'][6] = this.state['B'][2];
        this.state['B'][2] = this.state['D'][6];
        this.state['B'][5] = this.state['D'][3];
        this.state['B'][8] = this.state['D'][0];
        this.state['D'][0] = temp[0];
        this.state['D'][3] = temp[1];
        this.state['D'][6] = temp[2];
    }

    moveF() {
        this.rotateFace('F');
        const temp = [this.state['U'][6], this.state['U'][7], this.state['U'][8]];
        this.state['U'][6] = this.state['L'][8];
        this.state['U'][7] = this.state['L'][5];
        this.state['U'][8] = this.state['L'][2];
        this.state['L'][2] = this.state['D'][0];
        this.state['L'][5] = this.state['D'][1];
        this.state['L'][8] = this.state['D'][2];
        this.state['D'][0] = this.state['R'][6];
        this.state['D'][1] = this.state['R'][3];
        this.state['D'][2] = this.state['R'][0];
        this.state['R'][0] = temp[0];
        this.state['R'][3] = temp[1];
        this.state['R'][6] = temp[2];
    }

    moveB() {
        this.rotateFace('B');
        const temp = [this.state['U'][0], this.state['U'][1], this.state['U'][2]];
        this.state['U'][0] = this.state['R'][2];
        this.state['U'][1] = this.state['R'][5];
        this.state['U'][2] = this.state['R'][8];
        this.state['R'][2] = this.state['D'][8];
        this.state['R'][5] = this.state['D'][7];
        this.state['R'][8] = this.state['D'][6];
        this.state['D'][6] = this.state['L'][0];
        this.state['D'][7] = this.state['L'][3];
        this.state['D'][8] = this.state['L'][6];
        this.state['L'][0] = temp[2];
        this.state['L'][3] = temp[1];
        this.state['L'][6] = temp[0];
    }

    isSolved() {
        for (let face in this.state) {
            const centerColor = this.state[face][4];
            for (let sticker of this.state[face]) {
                if (sticker !== centerColor) return false;
            }
        }
        return true;
    }

    getStateString() {
        return Object.values(this.state).flat().join('');
    }
}

// ========== OPTIMIZED SOLVER ==========
class OptimizedSolver {
    constructor() {
        this.moves = ['U', "U'", 'U2', 'D', "D'", 'D2', 'R', "R'", 'R2', 
                     'L', "L'", 'L2', 'F', "F'", 'F2', 'B', "B'", 'B2'];
        
        this.phase2Moves = ['U', "U'", 'U2', 'D', "D'", 'D2', 'R2', 'L2', 'F2', 'B2'];
        
        this.inverse = {
            'U': "U'", "U'": 'U', 'U2': 'U2',
            'D': "D'", "D'": 'D', 'D2': 'D2',
            'R': "R'", "R'": 'R', 'R2': 'R2',
            'L': "L'", "L'": 'L', 'L2': 'L2',
            'F': "F'", "F'": 'F', 'F2': 'F2',
            'B': "B'", "B'": 'B', 'B2': 'B2'
        };
    }

    async solve(cube) {
        if (cube.isSolved()) return [];

        console.log("Starting optimized solve...");
        
        // Try IDA* with better heuristics
        const solution = await this.idaStar(cube.copy());
        if (solution && solution.length > 0) {
            return this.optimizeSolution(solution);
        }

        // Fallback to BFS if IDA* fails
        console.log("Using BFS fallback...");
        return await this.bfsSolve(cube.copy());
    }

    async idaStar(cube) {
        const bound = this.heuristic(cube);
        let path = [];
        
        for (let depth = bound; depth <= 25; depth++) {
            console.log(`Searching depth ${depth}...`);
            const result = await this.search(cube.copy(), path, 0, depth);
            
            if (result === true) {
                return path;
            }
            
            // Allow UI to update
            await new Promise(resolve => setTimeout(resolve, 10));
        }
        
        return null;
    }

    async search(cube, path, g, bound) {
        const f = g + this.heuristic(cube);
        
        if (f > bound) return f;
        if (cube.isSolved()) return true;
        
        let min = Infinity;
        const moves = this.getValidMoves(path);
        
        for (let move of moves) {
            cube.executeMove(move);
            path.push(move);
            
            const result = await this.search(cube, path, g + 1, bound);
            
            if (result === true) return true;
            if (result < min) min = result;
            
            path.pop();
            cube.executeMove(this.inverse[move]);
        }
        
        return min;
    }

    getValidMoves(path) {
        if (path.length === 0) return this.moves;
        
        const lastMove = path[path.length - 1];
        const lastFace = lastMove[0];
        
        // Don't repeat moves on the same face
        return this.moves.filter(move => {
            if (move[0] === lastFace) return false;
            if (move === this.inverse[lastMove]) return false;
            return true;
        });
    }

    heuristic(cube) {
        // Manhattan distance heuristic
        let distance = 0;
        
        // Count misplaced edge pieces
        const edges = this.getEdges(cube);
        edges.forEach(edge => {
            if (!this.isEdgeCorrect(edge)) distance++;
        });
        
        // Count misplaced corner pieces
        const corners = this.getCorners(cube);
        corners.forEach(corner => {
            if (!this.isCornerCorrect(corner)) distance++;
        });
        
        return Math.floor(distance / 4); // Approximate moves needed
    }

    getEdges(cube) {
        return [
            {colors: [cube.state['U'][1], cube.state['B'][1]], target: ['W', 'B']},
            {colors: [cube.state['U'][3], cube.state['L'][1]], target: ['W', 'O']},
            {colors: [cube.state['U'][5], cube.state['R'][1]], target: ['W', 'R']},
            {colors: [cube.state['U'][7], cube.state['F'][1]], target: ['W', 'G']},
            {colors: [cube.state['D'][1], cube.state['F'][7]], target: ['Y', 'G']},
            {colors: [cube.state['D'][3], cube.state['L'][7]], target: ['Y', 'O']},
            {colors: [cube.state['D'][5], cube.state['R'][7]], target: ['Y', 'R']},
            {colors: [cube.state['D'][7], cube.state['B'][7]], target: ['Y', 'B']},
            {colors: [cube.state['F'][3], cube.state['L'][5]], target: ['G', 'O']},
            {colors: [cube.state['F'][5], cube.state['R'][3]], target: ['G', 'R']},
            {colors: [cube.state['B'][3], cube.state['R'][5]], target: ['B', 'R']},
            {colors: [cube.state['B'][5], cube.state['L'][3]], target: ['B', 'O']}
        ];
    }

    getCorners(cube) {
        return [
            {colors: [cube.state['U'][0], cube.state['L'][0], cube.state['B'][2]], target: ['W', 'O', 'B']},
            {colors: [cube.state['U'][2], cube.state['B'][0], cube.state['R'][2]], target: ['W', 'B', 'R']},
            {colors: [cube.state['U'][6], cube.state['F'][0], cube.state['L'][2]], target: ['W', 'G', 'O']},
            {colors: [cube.state['U'][8], cube.state['R'][0], cube.state['F'][2]], target: ['W', 'R', 'G']},
            {colors: [cube.state['D'][0], cube.state['L'][6], cube.state['F'][6]], target: ['Y', 'O', 'G']},
            {colors: [cube.state['D'][2], cube.state['F'][8], cube.state['R'][6]], target: ['Y', 'G', 'R']},
            {colors: [cube.state['D'][6], cube.state['B'][8], cube.state['L'][8]], target: ['Y', 'B', 'O']},
            {colors: [cube.state['D'][8], cube.state['R'][8], cube.state['B'][6]], target: ['Y', 'R', 'B']}
        ];
    }

    isEdgeCorrect(edge) {
        const colors = edge.colors.sort().join('');
        const target = edge.target.sort().join('');
        return colors === target;
    }

    isCornerCorrect(corner) {
        const colors = corner.colors.sort().join('');
        const target = corner.target.sort().join('');
        return colors === target;
    }

    async bfsSolve(cube) {
        const visited = new Set();
        const queue = [{cube: cube.copy(), moves: []}];
        visited.add(cube.getStateString());
        
        let iterations = 0;
        const maxIterations = 30000;
        
        while (queue.length > 0 && iterations < maxIterations) {
            iterations++;
            
            const {cube: currentCube, moves} = queue.shift();
            
            if (currentCube.isSolved()) {
                console.log(`BFS found solution in ${iterations} iterations`);
                return moves;
            }
            
            if (moves.length >= 20) continue;
            
            for (let move of this.moves) {
                if (moves.length > 0) {
                    const lastMove = moves[moves.length - 1];
                    if (lastMove[0] === move[0]) continue;
                    if (move === this.inverse[lastMove]) continue;
                }
                
                const newCube = currentCube.copy();
                newCube.executeMove(move);
                
                const state = newCube.getStateString();
                if (!visited.has(state)) {
                    visited.add(state);
                    queue.push({cube: newCube, moves: [...moves, move]});
                }
            }
            
            if (iterations % 1000 === 0) {
                await new Promise(resolve => setTimeout(resolve, 10));
            }
        }
        
        console.log(`BFS searched ${iterations} states`);
        return [];
    }

    optimizeSolution(moves) {
        if (!moves || moves.length === 0) return [];
        
        let optimized = [...moves];
        let changed = true;
        
        while (changed) {
            changed = false;
            const newOptimized = [];
            
            let i = 0;
            while (i < optimized.length) {
                if (i < optimized.length - 1) {
                    const current = optimized[i];
                    const next = optimized[i + 1];
                    
                    // Remove cancelling moves
                    if (current === this.inverse[next]) {
                        i += 2;
                        changed = true;
                        continue;
                    }
                    
                    // Combine moves on same face
                    if (current[0] === next[0]) {
                        const combined = this.combineMoves(current, next);
                        if (combined) {
                            newOptimized.push(combined);
                            i += 2;
                            changed = true;
                            continue;
                        } else if (combined === '') {
                            i += 2;
                            changed = true;
                            continue;
                        }
                    }
                }
                
                newOptimized.push(optimized[i]);
                i++;
            }
            
            optimized = newOptimized;
        }
        
        return optimized;
    }

    combineMoves(move1, move2) {
        const face = move1[0];
        let total = 0;
        
        if (move1.includes("'")) total += 3;
        else if (move1.includes("2")) total += 2;
        else total += 1;
        
        if (move2.includes("'")) total += 3;
        else if (move2.includes("2")) total += 2;
        else total += 1;
        
        total = total % 4;
        
        if (total === 0) return '';
        if (total === 1) return face;
        if (total === 2) return face + '2';
        if (total === 3) return face + "'";
    }
}