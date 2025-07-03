let mode = 'encrypt';

function switchMode(newMode) {
    mode = newMode;
    document.querySelectorAll('.btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById('secretCode').style.display = mode === 'decrypt' ? 'block' : 'none';
}

function execute() {
    const text = document.getElementById('inputText').value;
    const code = document.getElementById('secretCode').value;
    const output = document.getElementById('output');
    
    output.textContent = 'Processing...';
    
    const data = mode === 'encrypt' ? { text } : { text, code };
    const url = mode === 'encrypt' ? '/encrypt' : '/decrypt';

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            output.textContent = `Error: ${data.error}`;
            output.style.color = '#ff0000';
        } else {
            output.textContent = data.result;
            output.style.color = '#00ff00';
        }
    })
    .catch(error => {
        output.textContent = 'Transmission failed!';
        output.style.color = '#ff0000';
    });
}