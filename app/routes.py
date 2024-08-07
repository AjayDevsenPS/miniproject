from flask import Flask, render_template, request, redirect, url_for, send_from_directory, current_app
from werkzeug.utils import secure_filename
import os
from .encryption import encrypt_message, decrypt_message
from .steganography import encode_message, decode_message
from PIL import Image

app = Flask(__name__)
app.config.from_object('config.Config')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = request.form['message']
    password = request.form['password']
    encrypted_message = encrypt_message(message, password)
    return render_template('index.html', encrypted_message=encrypted_message)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_message = request.form['encrypted_message']
    password = request.form['password']
    decrypted_message = decrypt_message(encrypted_message, password)
    return render_template('index.html', decrypted_message=decrypted_message)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        message = request.form['message']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            encoded_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'encoded_' + filename)
            encode_message(file_path, message, encoded_image_path)
            return send_from_directory(current_app.config['UPLOAD_FOLDER'], 'encoded_' + filename)
    return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
