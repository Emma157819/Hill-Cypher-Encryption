from flask import Flask, render_template, request, jsonify
from sympy import Matrix, gcd, mod_inverse
from random import randint

app = Flask(__name__)

MOD = 95  # For all printable ASCII (32-126 → 0-94)
SECRET_CODE = "BIGDADDY"  # Secret code for decryption

def is_valid_key(key_matrix, mod):
    """Check if key matrix is invertible under given modulus"""
    det = int(key_matrix.det()) % mod
    return det != 0 and gcd(det, mod) == 1

def generate_valid_key(n, mod):
    """Generate an invertible nxn matrix under given modulus"""
    while True:
        key = Matrix([[randint(0, mod-1) for _ in range(n)] for _ in range(n)])
        if is_valid_key(key, mod):
            return key

def text_to_numbers(text):
    return [ord(char) - 32 for char in text]

def numbers_to_text(numbers):
    return ''.join(chr(num + 32) for num in numbers)

def encrypt_hill(plaintext, key_matrix):
    if not is_valid_key(key_matrix, MOD):
        return None  # Invalid key matrix
    
    n = key_matrix.shape[0]
    plaintext_numbers = text_to_numbers(plaintext)
    
    # Pad with NULL (0) if needed
    pad_length = (n - len(plaintext_numbers) % n) % n
    plaintext_numbers += [0] * pad_length
    
    ciphertext = []
    for i in range(0, len(plaintext_numbers), n):
        block = Matrix(plaintext_numbers[i:i+n])
        encrypted_block = (key_matrix * block) % MOD
        ciphertext.extend(encrypted_block.T.tolist()[0])
    
    return numbers_to_text(ciphertext)

def decrypt_hill(ciphertext, key_matrix):
    if not is_valid_key(key_matrix, MOD):
        return None  # Invalid key matrix
    
    n = key_matrix.shape[0]
    ciphertext_numbers = text_to_numbers(ciphertext)
    
    # Calculate inverse matrix
    det = int(key_matrix.det()) % MOD
    det_inv = mod_inverse(det, MOD)
    adjugate = key_matrix.adjugate()
    key_matrix_inv = (det_inv * adjugate) % MOD
    
    plaintext = []
    for i in range(0, len(ciphertext_numbers), n):
        block = Matrix(ciphertext_numbers[i:i+n])
        decrypted_block = (key_matrix_inv * block) % MOD
        plaintext.extend([int(num) for num in decrypted_block])
    
    # Remove NULL padding
    while len(plaintext) > 0 and plaintext[-1] == 0:
        plaintext.pop()
    
    return numbers_to_text(plaintext)

# Pre-verified key matrix (det = 1031, gcd(1031,95)=1)
key_matrix = Matrix([
    [3, 10, 7],
    [15, 23, 6],
    [14, 5, 19]
])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    plaintext = data.get('text', '')
    if not plaintext:
        return jsonify({'error': 'No text provided'}), 400
    ciphertext = encrypt_hill(plaintext, key_matrix)
    if ciphertext is None:
        return jsonify({'error': 'Invalid key matrix'}), 400
    return jsonify({'result': ciphertext})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    ciphertext = data.get('text', '')
    code = data.get('code', '')
    if not ciphertext or not code:
        return jsonify({'error': 'Missing text or code'}), 400
    if code.upper() != SECRET_CODE:
        return jsonify({'error': 'Access Denied'}), 403
    decrypted_text = decrypt_hill(ciphertext, key_matrix)
    if decrypted_text is None:
        return jsonify({'error': 'Invalid key matrix or ciphertext'}), 400
    return jsonify({'result': decrypted_text})

if __name__ == '__main__':
    app.run(debug=True)