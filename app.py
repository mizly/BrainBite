import time
from flask import Flask, request, render_template, jsonify
from generate_video import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/generate', methods=['POST'])
def generate():
    text_input = request.form['text']
    timestamp = int(time.time())

    with open(f"data/input_{timestamp}.txt", "w", encoding='utf-8') as f: 
        f.write(text_input)
        f.close()

    voice = 'en_us_001'
    run_tts(timestamp, voice)
    transcription(timestamp)
    json_to_srt(timestamp)
    encode_video(timestamp)
    return render_template('video.html', timestamp=str(timestamp))

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if a file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to handle file uploads
@app.route('/upload-endpoint', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully!', 'filename': filename}), 200

    return jsonify({'message': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)