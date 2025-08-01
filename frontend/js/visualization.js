// frontend/js/visualization.js

class CubeVisualization {
    constructor(elementId) {
        this.element = document.getElementById(elementId);
        this.rotationX = -25;
        this.rotationY = 45;
        this.init();
    }
    
    init() {
        // Create face elements if they don't exist
        const faces = ['front', 'back', 'right', 'left', 'top', 'bottom'];
        const faceMap = {
            'front': 'F',
            'back': 'B',
            'right': 'R',
            'left': 'L',
            'top': 'U',
            'bottom': 'D'
        };
        
        faces.forEach(face => {
            let faceElement = this.element.querySelector(`.${face}`);
            if (!faceElement) {
                faceElement = document.createElement('div');
                faceElement.className = `face ${face}`;
                faceElement.dataset.face = faceMap[face];
                this.element.appendChild(faceElement);
            }
            
            // Create stickers
            faceElement.innerHTML = '';
            for (let i = 0; i < 9; i++) {
                const sticker = document.createElement('div');
                sticker.className = 'sticker';
                sticker.dataset.position = i;
                faceElement.appendChild(sticker);
            }
        });
        
        this.updateRotation();
    }
    
    update(state) {
        const faceMap = {
            'front': 'F',
            'back': 'B',
            'right': 'R',
            'left': 'L',
            'top': 'U',
            'bottom': 'D'
        };
        
        Object.entries(faceMap).forEach(([className, faceLetter]) => {
            const faceElement = this.element.querySelector(`.${className}`);
            const stickers = faceElement.querySelectorAll('.sticker');
            const faceColors = state[faceLetter];
            
            stickers.forEach((sticker, index) => {
                // Remove all color classes
                sticker.className = 'sticker';
                // Add the appropriate color class
                sticker.classList.add(faceColors[index]);
            });
        });
    }
    
    rotate(axis) {
        if (axis === 'x') {
            this.rotationX += 90;
        } else if (axis === 'y') {
            this.rotationY += 90;
        }
        this.updateRotation();
    }
    
    resetRotation() {
        this.rotationX = -25;
        this.rotationY = 45;
        this.updateRotation();
    }
    
    updateRotation() {
        this.element.style.transform = `rotateX(${this.rotationX}deg) rotateY(${this.rotationY}deg)`;
    }
    
    animateMove(move) {
        // Add animation class based on move
        const faceAnimations = {
            'U': 'rotate-u',
            "U'": 'rotate-u-prime',
            'D': 'rotate-d',
            "D'": 'rotate-d-prime',
            'R': 'rotate-r',
            "R'": 'rotate-r-prime',
            'L': 'rotate-l',
            "L'": 'rotate-l-prime',
            'F': 'rotate-f',
            "F'": 'rotate-f-prime',
            'B': 'rotate-b',
            "B'": 'rotate-b-prime'
        };
        
        if (faceAnimations[move]) {
            this.element.classList.add(faceAnimations[move]);
            setTimeout(() => {
                this.element.classList.remove(faceAnimations[move]);
            }, 300);
        }
    }
}