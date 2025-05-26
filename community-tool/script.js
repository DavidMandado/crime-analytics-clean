// index.html → script.js
document.getElementById('citizen-btn').onclick = () =>
  document.getElementById('login-modal').style.display = 'block';

document.getElementById('close-modal').onclick = () =>
  document.getElementById('login-modal').style.display = 'none';

document.getElementById('login-form').onsubmit = e => {
  e.preventDefault();
  // demo only
  window.location.href = 'feedback.html';
};

document.getElementById('police-btn').onclick = () =>
  window.location.href = 'restricted.html';
