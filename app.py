import time
from flask import Flask, request, render_template, jsonify, url_for
from generate_video import *
from process_text import process_text

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video/<int:timestamp>')
def video(timestamp):
    print("meow")
    return render_template('video.html', timestamp=str(timestamp))

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
    return str(timestamp)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if a file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to handle file uploads
@app.route('/upload-endpoint', methods=['POST'])
def upload_file():
    print(request.files)
    if 'resume' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the text from the uploaded file
        text = process_text(file_path)

        # Create a data payload for the generate function
        payload = {'text': text}
        
        generate_url = request.url_root + url_for('generate')

        # Send a POST request to the generate function
        response = requests.post(generate_url, data={'text': text})
        
        # You can handle the response from generate if needed
        if response.status_code == 200:
            return str(response.content.decode('utf-8'))
        else:
            return jsonify({'message': 'Error in generating response', 'details': response.json()}), 500

    return jsonify({'message': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)