const boardElement = document.getElementById('board');
let board = Array(9).fill(null);

function renderBoard() {
  boardElement.innerHTML = '';
  board.forEach((cell, idx) => {
    const btn = document.createElement('button');
    btn.textContent = cell || '';
    btn.disabled = !!cell;
    btn.addEventListener('click', () => handlePlayerMove(idx));
    boardElement.appendChild(btn);
  });
}

function handlePlayerMove(index) {
  if (board[index]) return;
  board[index] = 'X';
  renderBoard();
  sendMoveToBackend();
}

function sendMoveToBackend() {
  // fetch('/ai-chat/', {
  fetch('http://127.0.0.1:8000/ai-chat/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ board })
  })
    .then(res => res.json())
    .then(data => {
      board = data.board;
      renderBoard();
      updateChat('advisor-chat', data.advisor_messages);
      updateChat('ai-duo-chat', data.ai_duo_messages);
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

renderBoard();
