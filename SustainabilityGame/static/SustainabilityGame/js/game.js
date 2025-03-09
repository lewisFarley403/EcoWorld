document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    // Game settings
    const gridSize = 20;
    const gameSpeed = 100;
    
    // Game state
    let snake = [];
    let trash = {};
    let direction = 'right';
    let nextDirection = 'right';
    let score = 0;
    let trashCollected = 0;
    let gameRunning = false;
    let gameLoop;

    // Trash types
    const trashTypes = [
        { name: 'plastic', color: '#3498db', points: 10 },
        { name: 'paper', color: '#ecf0f1', points: 5 },
        { name: 'metal', color: '#7f8c8d', points: 15 },
        { name: 'glass', color: '#2ecc71', points: 20 }
    ];

    // Initialize game
    function initGame() {
        // Create initial snake
        snake = [
            {x: 5 * gridSize, y: 10 * gridSize},
            {x: 4 * gridSize, y: 10 * gridSize},
            {x: 3 * gridSize, y: 10 * gridSize}
        ];

        // Place initial trash
        placeTrash();

        // Reset scores
        score = 0;
        trashCollected = 0;

        // Update UI
        updateScore();
    }

    // Place a new trash item
    function placeTrash() {
        // Get random position
        const x = Math.floor(Math.random() * (canvas.width / gridSize)) * gridSize;
        const y = Math.floor(Math.random() * (canvas.height / gridSize)) * gridSize;

        // Check if position is occupied by snake
        const isOccupied = snake.some(segment => segment.x === x && segment.y === y);

        if (isOccupied) {
            // Try again if position is occupied
            placeTrash();
            return;
        }

        // Select random trash type
        const trashType = trashTypes[Math.floor(Math.random() * trashTypes.length)];

        // Place trash
        trash = {
            x: x,
            y: y,
            type: trashType
        };
    }

    // Update game state
    function update() {
        // Get next position based on direction
        let nextX = snake[0].x;
        let nextY = snake[0].y;

        // Update direction
        direction = nextDirection;

        // Calculate next position
        switch(direction) {
            case 'up':
                nextY -= gridSize;
                break;
            case 'down':
                nextY += gridSize;
                break;
            case 'left':
                nextX -= gridSize;
                break;
            case 'right':
                nextX += gridSize;
                break;
        }

        // Check for collision with walls
        if (nextX < 0 || nextY < 0 || nextX >= canvas.width || nextY >= canvas.height) {
            endGame();
            return;
        }

        // Check for collision with self
        if (snake.some(segment => segment.x === nextX && segment.y === nextY)) {
            endGame();
            return;
        }

        // Move snake
        snake.unshift({x: nextX, y: nextY});

        // Check for collision with trash
        if (nextX === trash.x && nextY === trash.y) {
            // Collect trash
            score += trash.type.points;
            trashCollected++;

            // Update UI
            updateScore();

            // Place new trash
            placeTrash();
        } else {
            // Remove tail if no trash was collected
            snake.pop();
        }
    }

    // Draw game
    function draw() {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw background
        ctx.fillStyle = '#f5f5f5';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Draw snake
        snake.forEach((segment, index) => {
            if (index === 0) {
                // Head
                ctx.fillStyle = '#4CAF50';
            } else {
                // Body
                ctx.fillStyle = '#81C784';
            }

            ctx.fillRect(segment.x, segment.y, gridSize, gridSize);

            // Draw border
            ctx.strokeStyle = '#388E3C';
            ctx.strokeRect(segment.x, segment.y, gridSize, gridSize);
        });

        // Draw trash
        ctx.fillStyle = trash.type.color;
        ctx.fillRect(trash.x, trash.y, gridSize, gridSize);
        ctx.strokeStyle = '#333';
        ctx.strokeRect(trash.x, trash.y, gridSize, gridSize);

        // Draw trash icon (simple representation)
        ctx.fillStyle = '#333';
        ctx.beginPath();
        ctx.moveTo(trash.x + 5, trash.y + 5);
        ctx.lineTo(trash.x + 15, trash.y + 5);
        ctx.lineTo(trash.x + 15, trash.y + 15);
        ctx.lineTo(trash.x + 5, trash.y + 15);
        ctx.closePath();
        ctx.fill();
    }

    // Update score display
    function updateScore() {
        document.getElementById('score').textContent = score;
        document.getElementById('trash-collected').textContent = trashCollected;
    }

    // End the game
    function endGame() {
        // Stop game loop
        clearInterval(gameLoop);
        gameRunning = false;

        // Display game over
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = 'white';
        ctx.font = '30px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Game Over!', canvas.width / 2, canvas.height / 2 - 30);
        ctx.font = '20px Arial';
        ctx.fillText(`Score: ${score}`, canvas.width / 2, canvas.height / 2 + 10);
        ctx.fillText(`Trash Collected: ${trashCollected}`, canvas.width / 2, canvas.height / 2 + 40);

        // Save score
        saveScore();
    }

    // Start the game
    function startGame() {
        if (gameRunning) return;

        initGame();
        gameRunning = true;
        gameLoop = setInterval(function() {
            update();
            draw();
        }, gameSpeed);
    }

    // Pause the game
    function pauseGame() {
        if (!gameRunning) {
            startGame();
            document.getElementById('pause-btn').textContent = 'Pause';
        } else {
            clearInterval(gameLoop);
            gameRunning = false;
            document.getElementById('pause-btn').textContent = 'Resume';

            // Display paused message
            ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = 'white';
            ctx.font = '30px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('Paused', canvas.width / 2, canvas.height / 2);
        }
    }

    // Save score to the server
    function saveScore() {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('/game/save_score/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                score: score
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.coins_earned) {
                displayCoinsEarned(data.coins_earned);
            }
        })
        .catch(error => console.error('Error saving score:', error));
    }

    // Display coins earned notification
    function displayCoinsEarned(coins) {
        const notification = document.createElement('div');
        notification.className = 'coin-notification';
        notification.innerHTML = `<img src="{% static 'SustainabilityGame/img/coin.png' %}" alt="Coin"> +${coins}`;
        document.querySelector('.game-container').appendChild(notification);

        setTimeout(() => {
            notification.classList.add('fade-out');
            setTimeout(() => notification.remove(), 1000);
        }, 2000);
    }

    // Event listeners
    document.addEventListener('keydown', function(event) {
        switch(event.key) {
            case 'ArrowUp':
                if (direction !== 'down') nextDirection = 'up';
                break;
            case 'ArrowDown':
                if (direction !== 'up') nextDirection = 'down';
                break;
            case 'ArrowLeft':
                if (direction !== 'right') nextDirection = 'left';
                break;
            case 'ArrowRight':
                if (direction !== 'left') nextDirection = 'right';
                break;
            case ' ':
                pauseGame();
                break;
        }
    });

    document.getElementById('start-btn').addEventListener('click', startGame);
    document.getElementById('pause-btn').addEventListener('click', pauseGame);

    // Initial draw
    draw();
});