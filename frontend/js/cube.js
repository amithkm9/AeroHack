// frontend/js/cube.js

class Cube {
    constructor() {
        this.reset();
    }
    
    reset() {
        this.state = {
            'U': Array(9).fill('W'),
            'D': Array(9).fill('Y'),
            'F': Array(9).fill('G'),
            'B': Array(9).fill('B'),
            'R': Array(9).fill('R'),
            'L': Array(9).fill('O')
        };
        this.moveHistory = [];
    }
    
    setState(newState) {
        this.state = JSON.parse(JSON.stringify(newState));
    }
    
    getState() {
        return JSON.parse(JSON.stringify(this.state));
    }
    
    rotateFaceClockwise(face) {
        const f = this.state[face];
        const temp = [...f];
        
        // Rotate corners
        f[0] = temp[6];
        f[2] = temp[0];
        f[8] = temp[2];
        f[6] = temp[8];
        
        // Rotate edges
        f[1] = temp[3];
        f[5] = temp[1];
        f[7] = temp[5];
        f[3] = temp[7];
    }
    
    executeMove(move) {
        const moves = {
            'U': () => this.moveU(),
            "U'": () => this.moveUprime(),
            'U2': () => { this.moveU(); this.moveU(); },
            'D': () => this.moveD(),
            "D'": () => this.moveDprime(),
            'D2': () => { this.moveD(); this.moveD(); },
            'R': () => this.moveR(),
            "R'": () => this.moveRprime(),
            'R2': () => { this.moveR(); this.moveR(); },
            'L': () => this.moveL(),
            "L'": () => this.moveLprime(),
            'L2': () => { this.moveL(); this.moveL(); },
            'F': () => this.moveF(),
            "F'": () => this.moveFprime(),
            'F2': () => { this.moveF(); this.moveF(); },
            'B': () => this.moveB(),
            "B'": () => this.moveBprime(),
            'B2': () => { this.moveB(); this.moveB(); }
        };
        
        if (moves[move]) {
            moves[move]();
            this.moveHistory.push(move);
        }
    }
    
    moveU() {
        this.rotateFaceClockwise('U');
        const temp = [this.state.F[0], this.state.F[1], this.state.F[2]];
        this.state.F[0] = this.state.R[0];
        this.state.F[1] = this.state.R[1];
        this.state.F[2] = this.state.R[2];
        this.state.R[0] = this.state.B[0];
        this.state.R[1] = this.state.B[1];
        this.state.R[2] = this.state.B[2];
        this.state.B[0] = this.state.L[0];
        this.state.B[1] = this.state.L[1];
        this.state.B[2] = this.state.L[2];
        this.state.L[0] = temp[0];
        this.state.L[1] = temp[1];
        this.state.L[2] = temp[2];
    }
    
    moveUprime() {
        this.moveU();
        this.moveU();
        this.moveU();
    }
    
    moveD() {
        this.rotateFaceClockwise('D');
        const temp = [this.state.F[6], this.state.F[7], this.state.F[8]];
        this.state.F[6] = this.state.L[6];
        this.state.F[7] = this.state.L[7];
        this.state.F[8] = this.state.L[8];
        this.state.L[6] = this.state.B[6];
        this.state.L[7] = this.state.B[7];
        this.state.L[8] = this.state.B[8];
        this.state.B[6] = this.state.R[6];
        this.state.B[7] = this.state.R[7];
        this.state.B[8] = this.state.R[8];
        this.state.R[6] = temp[0];
        this.state.R[7] = temp[1];
        this.state.R[8] = temp[2];
    }
    
    moveDprime() {
        this.moveD();
        this.moveD();
        this.moveD();
    }
    
    moveR() {
        this.rotateFaceClockwise('R');
        const temp = [this.state.F[2], this.state.F[5], this.state.F[8]];
        this.state.F[2] = this.state.D[2];
        this.state.F[5] = this.state.D[5];
        this.state.F[8] = this.state.D[8];
        this.state.D[2] = this.state.B[6];
        this.state.D[5] = this.state.B[3];
        this.state.D[8] = this.state.B[0];
        this.state.B[6] = this.state.U[2];
        this.state.B[3] = this.state.U[5];
        this.state.B[0] = this.state.U[8];
        this.state.U[2] = temp[0];
        this.state.U[5] = temp[1];
        this.state.U[8] = temp[2];
    }
    
    moveRprime() {
        this.moveR();
        this.moveR();
        this.moveR();
    }
    
    moveL() {
        this.rotateFaceClockwise('L');
        const temp = [this.state.F[0], this.state.F[3], this.state.F[6]];
        this.state.F[0] = this.state.U[0];
        this.state.F[3] = this.state.U[3];
        this.state.F[6] = this.state.U[6];
        this.state.U[0] = this.state.B[8];
        this.state.U[3] = this.state.B[5];
        this.state.U[6] = this.state.B[2];
        this.state.B[8] = this.state.D[0];
        this.state.B[5] = this.state.D[3];
        this.state.B[2] = this.state.D[6];
        this.state.D[0] = temp[0];
        this.state.D[3] = temp[1];
        this.state.D[6] = temp[2];
    }
    
    moveLprime() {
        this.moveL();
        this.moveL();
        this.moveL();
    }
    
    moveF() {
        this.rotateFaceClockwise('F');
        const temp = [this.state.U[6], this.state.U[7], this.state.U[8]];
        this.state.U[6] = this.state.L[8];
        this.state.U[7] = this.state.L[5];
        this.state.U[8] = this.state.L[2];
        this.state.L[8] = this.state.D[2];
        this.state.L[5] = this.state.D[1];
        this.state.L[2] = this.state.D[0];
        this.state.D[2] = this.state.R[0];
        this.state.D[1] = this.state.R[3];
        this.state.D[0] = this.state.R[6];
        this.state.R[0] = temp[0];
        this.state.R[3] = temp[1];
        this.state.R[6] = temp[2];
    }
    
    moveFprime() {
        this.moveF();
        this.moveF();
        this.moveF();
    }
    
    moveB() {
        this.rotateFaceClockwise('B');
        const temp = [this.state.U[0], this.state.U[1], this.state.U[2]];
        this.state.U[0] = this.state.R[2];
        this.state.U[1] = this.state.R[5];
        this.state.U[2] = this.state.R[8];
        this.state.R[2] = this.state.D[8];
        this.state.R[5] = this.state.D[7];
        this.state.R[8] = this.state.D[6];
        this.state.D[8] = this.state.L[6];
        this.state.D[7] = this.state.L[3];
        this.state.D[6] = this.state.L[0];
        this.state.L[6] = temp[0];
        this.state.L[3] = temp[1];
        this.state.L[0] = temp[2];
    }
    
    moveBprime() {
        this.moveB();
        this.moveB();
        this.moveB();
    }
    
    isSolved() {
        for (let face in this.state) {
            const centerColor = this.state[face][4];
            for (let i = 0; i < 9; i++) {
                if (this.state[face][i] !== centerColor) {
                    return false;
                }
            }
        }
        return true;
    }
}