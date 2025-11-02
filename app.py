import os
import subprocess
from flask import Flask, render_template, request, jsonify, Response
from prediction_runner import run_prediction_stream

app = Flask(__name__)

# Path to store uploaded files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return "File uploaded successfully", 200

@app.route('/run-prediction', methods=['GET'])
def run_prediction():
    def generate():
        for output in run_prediction_stream():
            yield f"{output}<br>\n"
    
    return Response(generate(), mimetype='text/html')

if __name__ == "__main__":
    app.run(debug=True)
