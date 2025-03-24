// Log confirmation
console.log("Script loaded!");

// Generate a dynamic session ID
const sessionId = localStorage.getItem('sessionId') || Math.random().toString(36).substr(2, 9);
localStorage.setItem('sessionId', sessionId);

// Form submission handler
document.getElementById('codeForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const prompt = document.getElementById('prompt').value.trim();
  const language = document.getElementById('language').value;
  const outputElement = document.getElementById('output');
  const submitButton = document.getElementById('submitButton');

  if (!prompt) {
    outputElement.textContent = "Please enter a valid prompt!";
    return;
  }

  // Show loading message and disable the button
  outputElement.textContent = 'Generating code...';
  submitButton.disabled = true;

  try {
    const response = await fetch('http://localhost:8000/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, language, session_id: sessionId }),
    });

    if (!response.ok) throw new Error(`Server Error: ${response.status}`);

    const data = await response.json();
    outputElement.textContent = data.code || 'Error: Unable to generate code.';

    // Flip open the output panel with delay
    document.querySelector('.output-container').classList.remove('flip');
    setTimeout(() => document.querySelector('.output-container').classList.add('flip'), 100);
  } catch (error) {
    console.error('Error:', error);
    outputElement.textContent = `Error: ${error.message}`;
  } finally {
    submitButton.disabled = false;
  }
});

// Copy to clipboard
document.getElementById('copyButton').addEventListener('click', () => {
  const code = document.getElementById('output').textContent.trim();
  if (code) {
    navigator.clipboard.writeText(code).then(() => {
      const copyBtn = document.getElementById('copyButton');
      copyBtn.textContent = 'Copied!';
      setTimeout(() => copyBtn.textContent = 'Copy Code', 2000);
    });
  }
});

// Button hover glow effects
document.querySelectorAll('button').forEach(button => {
  button.addEventListener('mouseenter', () => button.style.boxShadow = '0 0 15px rgba(0, 255, 255, 0.8)');
  button.addEventListener('mouseleave', () => button.style.boxShadow = 'none');
});

// Glass container glow effects
document.querySelectorAll('.glass').forEach(container => {
  container.addEventListener('mouseenter', () => {
    container.style.boxShadow = '0 0 30px rgba(0, 255, 255, 0.4), 0 0 60px rgba(138, 43, 226, 0.2)';
  });
  container.addEventListener('mouseleave', () => {
    container.style.boxShadow = '0 0 20px rgba(0, 255, 255, 0.2), 0 0 40px rgba(138, 43, 226, 0.1)';
  });
});
