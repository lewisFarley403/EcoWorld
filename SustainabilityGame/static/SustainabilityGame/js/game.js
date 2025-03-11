// Game Configuration
const CONFIG = {
    grid: { size: 25, speed: 100 },
    canvas: { width: 600, height: 400 },
    colors: {
        background: '#f5f5f5',
        snake: { head: '#4CAF50', body: '#81C784', border: '#388E3C' },
        overlay: 'rgba(0, 0, 0, 0.7)'
    },
    trash: [
        { name: 'plastic', color: '#3498db', points: 10 },
        { name: 'paper', color: '#ecf0f1', points: 5 },
        { name: 'metal', color: '#7f8c8d', points: 15 },
        { name: 'glass', color: '#2ecc71', points: 20 }
    ]
};

const trashImages = {
    'plastic': new Image(),
    'paper': new Image(),
    'metal': new Image(),
    'glass': new Image()
};

trashImages.plastic.src = '/static/SustainabilityGame/img/trash/plastic-bottle.png';
trashImages.paper.src = '/static/SustainabilityGame/img/trash/paper.png';
trashImages.metal.src = '/static/SustainabilityGame/img/trash/metal-can.png';
trashImages.glass.src = '/static/SustainabilityGame/img/trash/glass-bottle.png';

class Game {
    constructor() {
        this.entryCost = 0; // Starting cost
        this.playCount = 0;
        this.initializeCanvas();
        this.bindElements();
        this.setupEventListeners();
        this.state = new GameState();
        this.renderer = new Renderer(this.ctx);
        this.lastRender = 0;
        this.draw();
    }

    initializeCanvas() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvas.width = CONFIG.canvas.width;
        this.canvas.height = CONFIG.canvas.height;
    }

    bindElements() {
        this.elements = {
            score: document.getElementById('score'),
            trashCount: document.getElementById('trash-collected'),
            startBtn: document.getElementById('start-btn'),
            pauseBtn: document.getElementById('pause-btn')
        };
    }

    setupEventListeners() {
        document.addEventListener('keydown', this.handleInput.bind(this));
        this.elements.startBtn.addEventListener('click', () => this.start());
        this.elements.pauseBtn.addEventListener('click', () => this.togglePause());
        
        // Add touch controls
        let touchStart = { x: 0, y: 0 };
        this.canvas.addEventListener('touchstart', (e) => {
            touchStart.x = e.touches[0].clientX;
            touchStart.y = e.touches[0].clientY;
        });
        
        this.canvas.addEventListener('touchmove', (e) => {
            if (!this.state.isRunning) return;
            const touchEnd = { 
                x: e.touches[0].clientX, 
                y: e.touches[0].clientY 
            };
            this.handleSwipe(touchStart, touchEnd);
            e.preventDefault();
        });
    }

    handleSwipe(start, end) {
        const dx = end.x - start.x;
        const dy = end.y - start.y;
        
        if (Math.abs(dx) > Math.abs(dy)) {
            if (dx > 0 && this.state.direction !== 'left') this.state.nextDirection = 'right';
            else if (dx < 0 && this.state.direction !== 'right') this.state.nextDirection = 'left';
        } else {
            if (dy > 0 && this.state.direction !== 'up') this.state.nextDirection = 'down';
            else if (dy < 0 && this.state.direction !== 'down') this.state.nextDirection = 'up';
        }
    }

    handleInput(event) {
        const keyActions = {
            'ArrowUp': () => this.state.direction !== 'down' && (this.state.nextDirection = 'up'),
            'ArrowDown': () => this.state.direction !== 'up' && (this.state.nextDirection = 'down'),
            'ArrowLeft': () => this.state.direction !== 'right' && (this.state.nextDirection = 'left'),
            'ArrowRight': () => this.state.direction !== 'left' && (this.state.nextDirection = 'right'),
            ' ': () => this.togglePause()
        };

        if (keyActions[event.key]) {
            keyActions[event.key]();
            event.preventDefault();
        }
    }

    start() {
        if (this.state.isRunning) return;

        this.state.reset();
        this.state.isRunning = true;
        requestAnimationFrame(this.gameLoop.bind(this));
    }

    gameLoop(timestamp) {
        if (!this.state.isRunning) return;

        if (timestamp - this.lastRender >= CONFIG.grid.speed) {
            this.update();
            this.draw();
            this.lastRender = timestamp;
        }

        requestAnimationFrame(this.gameLoop.bind(this));
    }

    update() {
        const nextPosition = this.state.getNextPosition();

        if (this.checkCollision(nextPosition)) {
            this.end();
            return;
        }

        // Move snake
        this.state.moveSnake(nextPosition);

        // Check for trash collection
        if (this.state.hasCollectedTrash(nextPosition)) {
            this.handleTrashCollection();
        }
    }


    checkCollision(position) {
        return this.state.isOutOfBounds(position) || 
               this.state.hasHitSelf(position);
    }

    handleTrashCollection() {
        this.state.updateScore();
        this.updateUI();
        // Don't remove tail when collecting trash
        this.state.snake.push(this.state.snake[this.state.snake.length - 1]);
        this.state.placeNewTrash();
    }

    end() {
        this.state.isRunning = false;
        // Make sure score is properly calculated before saving
        const finalScore = {
            score: this.state.score,
            trashCollected: this.state.trashCollected
        };
        // Force immediate score save
        this.saveScore(finalScore);
    }

    togglePause() {
        this.state.isRunning = !this.state.isRunning;
        this.elements.pauseBtn.textContent = this.state.isRunning ? 'Pause' : 'Resume';
        
        if (!this.state.isRunning) {
            this.renderer.drawPaused();
        } else {
            requestAnimationFrame(this.gameLoop.bind(this));
        }
    }

    draw() {
        this.renderer.clear();
        this.renderer.drawBackground();
        this.renderer.drawSnake(this.state.snake);
        this.renderer.drawTrash(this.state.trash);
    }

    updateUI() {
        this.elements.score.textContent = this.state.score;
        this.elements.trashCount.textContent = this.state.trashCollected;
    }

    showGameOverPopup(coinsEarned) {
        const overlay = document.createElement('div');
        overlay.className = 'game-over-overlay';

        const popup = document.createElement('div');
        popup.className = 'game-over-popup';

        popup.innerHTML = `
            <h2>Game Over!</h2>
            <div class="score-details">
                <p>Your Score: <strong>${this.state.score}</strong></p>
                <p>Trash Collected: <strong>${this.state.trashCollected}</strong></p>
                <p>Coins Earned: <strong>${coinsEarned}</strong></p>
            </div>
            <div class="game-over-buttons">
                <a href="/ecoworld/dashboard" class="home-button">Back to Home</a>
            </div>
        `;

        overlay.appendChild(popup);
        document.querySelector('.game-container').appendChild(overlay);
    }


    async saveScore() {
        try {
            // Get CSRF token from meta tag
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Make sure CSRF token exists
            if (!csrftoken) {
                console.error('CSRF token not found');
                return;
            }

            const response = await fetch('/game/save_score/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    score: this.state.score,
                    trashCollected: this.state.trashCollected
                })
            });

            const data = await response.json();
            if (data.status === 'success') {
                data.coins_earned = Math.floor(this.state.trashCollected * (this.state.score/20));
                this.showGameOverPopup(data.coins_earned);
            }
        } catch (error) {
            console.error('Error saving score:', error);
            // Show popup even if save fails
            this.showGameOverPopup(0);
        }
    }
}

class GameState {
    constructor() {
        this.reset();
    }

    reset() {
        this.snake = [
            {x: 5 * CONFIG.grid.size, y: 10 * CONFIG.grid.size},
            {x: 4 * CONFIG.grid.size, y: 10 * CONFIG.grid.size},
            {x: 3 * CONFIG.grid.size, y: 10 * CONFIG.grid.size}
        ];
        this.direction = 'right';
        this.nextDirection = 'right';
        this.score = 0;
        this.trashCollected = 0;
        this.isRunning = false;
        this.placeNewTrash();
    }

    getNextPosition() {
        const head = this.snake[0];
        const movements = {
            up: { x: 0, y: -CONFIG.grid.size },
            down: { x: 0, y: CONFIG.grid.size },
            left: { x: -CONFIG.grid.size, y: 0 },
            right: { x: CONFIG.grid.size, y: 0 }
        };
        this.direction = this.nextDirection;
        const move = movements[this.direction];
        return { x: head.x + move.x, y: head.y + move.y };
    }

    moveSnake(nextPosition) {
        this.snake.unshift(nextPosition);
        // Only remove the tail if we haven't collected trash
        if (!this.hasCollectedTrash(nextPosition)) {
            this.snake.pop();
        }
    }


    placeNewTrash() {
        const x = Math.floor(Math.random() * (CONFIG.canvas.width / CONFIG.grid.size)) * CONFIG.grid.size;
        const y = Math.floor(Math.random() * (CONFIG.canvas.height / CONFIG.grid.size)) * CONFIG.grid.size;
        const type = CONFIG.trash[Math.floor(Math.random() * CONFIG.trash.length)];
        this.trash = { x, y, type };
    }

    hasCollectedTrash(position) {
        return position.x === this.trash.x && position.y === this.trash.y;
    }

    updateScore() {
        this.score += this.trash.type.points;
        this.trashCollected++;
    }

    isOutOfBounds(position) {
        return position.x < 0 || position.y < 0 ||
               position.x >= CONFIG.canvas.width ||
               position.y >= CONFIG.canvas.height;
    }

    hasHitSelf(position) {
        return this.snake.some(segment =>
            segment.x === position.x && segment.y === position.y
        );
    }
}

class Renderer {
    constructor(ctx) {
        this.ctx = ctx;
    }

    clear() {
        this.ctx.clearRect(0, 0, CONFIG.canvas.width, CONFIG.canvas.height);
    }

    drawBackground() {
        this.ctx.fillStyle = CONFIG.colors.background;
        this.ctx.fillRect(0, 0, CONFIG.canvas.width, CONFIG.canvas.height);
    }

    drawSnake(snake) {
        snake.forEach((segment, index) => {
            this.ctx.fillStyle = index === 0 ? CONFIG.colors.snake.head : CONFIG.colors.snake.body;
            this.ctx.fillRect(segment.x, segment.y, CONFIG.grid.size, CONFIG.grid.size);
            this.ctx.strokeStyle = CONFIG.colors.snake.border;
            this.ctx.strokeRect(segment.x, segment.y, CONFIG.grid.size, CONFIG.grid.size);
        });
    }

    drawTrash(trash) {
        this.ctx.drawImage(trashImages[trash.type.name], trash.x, trash.y, CONFIG.grid.size, CONFIG.grid.size);
    }

    drawGameOver() {
        this.ctx.fillStyle = CONFIG.colors.overlay;
        this.ctx.fillRect(0, 0, CONFIG.canvas.width, CONFIG.canvas.height);
        this.ctx.fillStyle = 'white';
        this.ctx.font = '30px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('Game Over!', CONFIG.canvas.width / 2, CONFIG.canvas.height / 2);
    }

    drawPaused() {
        this.ctx.fillStyle = CONFIG.colors.overlay;
        this.ctx.fillRect(0, 0, CONFIG.canvas.width, CONFIG.canvas.height);
        this.ctx.fillStyle = 'white';
        this.ctx.font = '30px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('Paused', CONFIG.canvas.width / 2, CONFIG.canvas.height / 2);
    }

    showCollectionEffect(position) {
        // Add visual feedback for trash collection
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        this.ctx.beginPath();
        this.ctx.arc(position.x + CONFIG.grid.size/2, position.y + CONFIG.grid.size/2, CONFIG.grid.size, 0, Math.PI * 2);
        this.ctx.fill();
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => new Game());