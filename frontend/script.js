const boardElement = document.getElementById('board');
let board = Array(9).fill(null);
let isLoading = false;
let isEnd = false;
let scoreX = 0;
let scoreO = 0;

function renderBoard() {
  boardElement.innerHTML = '';
  board.forEach((cell, idx) => {
    const btn = document.createElement('button');
    btn.textContent = cell || '';
    btn.disabled = !!cell || isLoading;
    btn.addEventListener('click', () => handlePlayerMove(idx));
    boardElement.appendChild(btn);
  });
}

function handlePlayerMove(index) {
  if (board[index] || isLoading) return;
  board[index] = 'X';
  renderBoard();
  sendMoveToBackend();
}

function sendMoveToBackend() {
  isLoading = true;
  renderBoard();
  fetch('http://127.0.0.1:8000/ai-chat/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ board })
  })
    .then(res => res.json())
    .then(data => {
      board = data.board;
      updateChat('advisor-chat', data.advisor_messages);
      updateChat('ai-duo-chat', data.ai_duo_messages);
      if (data.winner) {
        isEnd = true;
        handleWinner(data.winner);
      }
    })
    .catch(err => {
      console.error('Chyba:', err);
      alert('Nepodařilo se spojit se serverem');
    })
    .finally(() => {
      if (!isEnd) {
      isLoading = false;
      }
      renderBoard();
    });
}

function updateChat(chatId, messages) {
  const el = document.getElementById(chatId);
  el.innerHTML = '';
  messages.forEach(msg => {
    const p = document.createElement('div');
    p.className = 'message ' + (msg.side === 'left' ? 'left' : 'right');
    p.textContent = msg.text;
    el.appendChild(p);
  });
}

function handleWinner(winner) {
  if (winner === 'X') {
    scoreX++;
  } else if (winner === 'O') {
    scoreO++;
  }
  updateScore();
}

function updateScore() {
  document.getElementById('score-x').textContent = scoreX;
  document.getElementById('score-o').textContent = scoreO;
}

function resetGame() {
  //console.log("resetGame()");
  board = Array(9).fill(null);
  isLoading = false;
  isEnd = false;
  renderBoard();
  document.getElementById('advisor-chat').innerHTML = '';
  document.getElementById('ai-duo-chat').innerHTML = '';
}

renderBoard();
document.getElementById('new-game-btn').addEventListener('click', resetGame);
