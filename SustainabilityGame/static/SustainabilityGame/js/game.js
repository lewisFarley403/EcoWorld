// Game Configuration object containing all game settings
const CONFIG = {
    grid: { size: 25, speed: 100 }, // Grid cell size and game speed
    canvas: { width: 600, height: 400 }, // Canvas dimensions
    colors: {
        background: '#f5f5f5', // Light gray background
        snake: {
            head: '#4CAF50', // Green head
            body: '#81C784', // Lighter green body
            border: '#388E3C' // Dark green border
        },
        overlay: 'rgba(0, 0, 0, 0.7)' // Semi-transparent black overlay
    },
    trash: [ // Different types of collectible trash with points
        { name: 'plastic', color: '#3498db', points: 10 },
        { name: 'paper', color: '#ecf0f1', points: 5 },
        { name: 'metal', color: '#7f8c8d', points: 15 },
        { name: 'glass', color: '#2ecc71', points: 20 }
    ],
    aspectRatio: 1.5, // width/height ratio to maintain
    minWidth: 100,    // minimum canvas width
    maxWidth: 800     // maximum canvas width
};

// Load trash images for each type
const trashImages = {
    'plastic': new Image(),
    'paper': new Image(),
    'metal': new Image(),
    'glass': new Image()
};

// Set image sources for each trash type
trashImages.plastic.src = '/static/SustainabilityGame/img/trash/plastic-bottle.png';
trashImages.paper.src = '/static/SustainabilityGame/img/trash/paper.png';
trashImages.metal.src = '/static/SustainabilityGame/img/trash/metal-can.png';
trashImages.glass.src = '/static/SustainabilityGame/img/trash/glass-bottle.png';

// Main Game class handling game logic and rendering
class Game {
    constructor() {
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

        const resizeCanvas = () => {
            const containerWidth = this.canvas.parentElement.clientWidth;
            let newWidth = Math.min(Math.max(containerWidth * 0.95, CONFIG.minWidth), CONFIG.maxWidth);
            let newHeight = newWidth / CONFIG.aspectRatio;

            this.canvas.width = newWidth-(newWidth*0.05);

            // Adjust grid size to maintain similar number of cells
            CONFIG.grid.size = Math.floor(newWidth / 24); // 24 cells across
        };

        // Initial resize
        resizeCanvas();

        // Add resize listener
        window.addEventListener('resize', resizeCanvas);
    }

    bindElements() {
        this.elements = {
            score: document.getElementById('score'),
            trashCount: document.getElementById('trash-collected'),
            startBtn: document.getElementById('start-btn'),
            pauseBtn: document.getElementById('pause-btn')
        };
    }

    // Set up keyboard and touch input handlers
    setupEventListeners() {
        document.addEventListener('keydown', this.handleInput.bind(this));
        this.elements.startBtn.addEventListener('click', () => this.start());
        this.elements.pauseBtn.addEventListener('click', () => this.togglePause());

        // Touch controls for mobile play
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

    // Process swipe gestures for mobile controls
    handleSwipe(start, end) {
        const dx = end.x - start.x;
        const dy = end.y - start.y;

        // Determine swipe direction and update snake movement
        if (Math.abs(dx) > Math.abs(dy)) {
            if (dx > 0 && this.state.direction !== 'left') this.state.nextDirection = 'right';
            else if (dx < 0 && this.state.direction !== 'right') this.state.nextDirection = 'left';
        } else {
            if (dy > 0 && this.state.direction !== 'up') this.state.nextDirection = 'down';
            else if (dy < 0 && this.state.direction !== 'down') this.state.nextDirection = 'up';
        }
    }

    // Handle keyboard input for snake control
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

    // Start new game
    start() {
        if (this.state.isRunning) return;
        this.state.reset();
        this.state.isRunning = true;
        requestAnimationFrame(this.gameLoop.bind(this));
    }

    // Main game loop
    gameLoop(timestamp) {
        if (!this.state.isRunning) return;

        if (timestamp - this.lastRender >= CONFIG.grid.speed) {
            this.update();
            this.draw();
            this.lastRender = timestamp;
        }

        requestAnimationFrame(this.gameLoop.bind(this));
    }

    // Update game state each frame
    update() {
        const nextPosition = this.state.getNextPosition();

        if (this.checkCollision(nextPosition)) {
            this.end();
            return;
        }

        // Move snake and check for trash collection
        this.state.moveSnake(nextPosition);
        if (this.state.hasCollectedTrash(nextPosition)) {
            this.handleTrashCollection();
        }
    }

    // Check for collisions with walls or self
    checkCollision(position) {
        return this.state.isOutOfBounds(position) ||
            this.state.hasHitSelf(position);
    }

    // Handle trash collection and scoring
    handleTrashCollection() {
        this.state.updateScore();
        this.updateUI();
        this.state.snake.push(this.state.snake[this.state.snake.length - 1]);
        this.state.placeNewTrash();
    }

    // End game and save score
    end() {
        this.state.isRunning = false;
        const finalScore = {
            score: this.state.score,
            trashCollected: this.state.trashCollected
        };
        this.saveScore(finalScore);
    }

    // Toggle game pause state
    togglePause() {
        this.state.isRunning = !this.state.isRunning;
        this.elements.pauseBtn.textContent = this.state.isRunning ? 'Pause' : 'Resume';

        if (!this.state.isRunning) {
            this.renderer.drawPaused();
        } else {
            requestAnimationFrame(this.gameLoop.bind(this));
        }
    }

    // Draw current game state
    draw() {
        this.renderer.clear();
        this.renderer.drawBackground();
        this.renderer.drawSnake(this.state.snake);
        this.renderer.drawTrash(this.state.trash);
    }

    // Update score display
    updateUI() {
        this.elements.score.textContent = this.state.score;
        this.elements.trashCount.textContent = this.state.trashCollected;
    }

    // Display game over popup with score
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

    // Save score to server
    async saveScore() {
        try {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
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
                data.coins_earned = this.calculateCoins(this.state.score);
                this.showGameOverPopup(data.coins_earned);
            }
        } catch (error) {
            console.error('Error saving score:', error);
            this.showGameOverPopup(0);
        }
    }

    // Calculate coins earned based on score
    calculateCoins(score) {
        if (score < 150) return 0;
        let a = 4;
        let b = 0.005;
        return Math.floor(a * Math.exp(b * (score - 150)));
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
        const canvas = document.getElementById('gameCanvas');
        let x, y;
        let validPosition = false;

        while (!validPosition) {
            // Limit the placement area by subtracting grid size
            x = Math.floor(Math.random() * ((canvas.width - CONFIG.grid.size) / CONFIG.grid.size)) * CONFIG.grid.size;
            y = Math.floor(Math.random() * ((canvas.height - CONFIG.grid.size) / CONFIG.grid.size)) * CONFIG.grid.size;

            validPosition = !this.snake.some(segment =>
                segment.x === x && segment.y === y
            );
        }

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
        const canvas = document.getElementById('gameCanvas');
        return position.x < 0 || position.y < 0 ||
            position.x + CONFIG.grid.size > canvas.width ||
            position.y + CONFIG.grid.size > canvas.height;
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
        const canvas = document.getElementById('gameCanvas');
        this.ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    drawBackground() {
        const canvas = document.getElementById('gameCanvas');
        this.ctx.fillStyle = CONFIG.colors.background;
        this.ctx.fillRect(0, 0, canvas.width, canvas.height);
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
        const canvas = document.getElementById('gameCanvas');
        this.ctx.fillStyle = CONFIG.colors.overlay;
        this.ctx.fillRect(0, 0, canvas.width, canvas.height);
        this.ctx.fillStyle = 'white';
        this.ctx.font = '30px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('Game Over!', canvas.width / 2, canvas.height / 2);
    }

    drawPaused() {
        const canvas = document.getElementById('gameCanvas');
        this.ctx.fillStyle = CONFIG.colors.overlay;
        this.ctx.fillRect(0, 0, canvas.width, canvas.height);
        this.ctx.fillStyle = 'white';
        this.ctx.font = '30px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('Paused', canvas.width / 2, canvas.height / 2);
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => new Game());

