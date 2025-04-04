const cells = document.querySelectorAll('.cell');
const currentPlayerDisplay = document.getElementById('currentPlayer');
const winnerMessageDisplay = document.getElementById('winnerMessage');
const resetButton = document.getElementById('resetButton');

function handleCellClick(event) {
    const cell = event.target;
    const index = cell.dataset.index;

    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ index: parseInt(index) }),
    })
    .then(response => response.json())
    .then(data => {
        updateBoard(data.board, data.current_player, data.winner);
    });
}

function updateBoard(board, currentPlayer, winner) {
    cells.forEach((cell, index) => {
        cell.textContent = board[index];
        cell.classList.remove('x', 'o', 'disabled');
        if(board[index] == 'X'){
            cell.classList.add('x');
        } else if (board[index] == 'O'){
            cell.classList.add('o');
        }
        if (board[index] !== ''){
            cell.classList.add('disabled');
        }
    });

    currentPlayerDisplay.textContent = `Current Player: ${currentPlayer}`;
    winnerMessageDisplay.textContent = winner ? (winner === 'Tie' ? "It's a tie!" : `${winner} wins!`) : '';
}

function resetGame() {
    fetch('/')
    .then(response => response.text())
    .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newBoard = doc.querySelectorAll('.cell');
        const newPlayer = doc.getElementById('currentPlayer').textContent.split(': ')[1];
        const newWinner = doc.getElementById('winnerMessage').textContent;
        updateBoard(Array.from(newBoard).map(cell => cell.textContent), newPlayer, newWinner);
    });
}

cells.forEach(cell => cell.addEventListener('click', handleCellClick));
resetButton.addEventListener('click', resetGame);