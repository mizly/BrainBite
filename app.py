import time
from flask import Flask, request, render_template, jsonify, url_for
from generate_video import *
from process_text import process_text
from gemini import *

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
    video_style = request.form['video-style']
    video_source = request.form['video-source']
    narrator = request.form['narrator']
    timestamp = int(time.time())

    style_to_function = {
        'nba': nbaOutput,
        'fortnite': fortniteOutput,
        'brainrot': brainrotOutput,
        'aita': redditOutput,
        'eli5': eli5Output,
        "none": unmodifiedOutput
    }

    style_to_voice = {
        'nba': 'en_us_001',
        'fortnite': 'en_us_001',
        'brainrot': 'en_us_001',
        'aita': 'en_us_001',
        'eli5': 'en_us_001',
        "none": 'en_us_001'
    }

    video_source_to_max_random = {
        "subway": 1800,
        "minecraft": 900,
        "soap": 600,
        "familyguy": 600,
        "cooking": 900,
        "breakingbad": 1800
    }

    output_function = style_to_function[video_style]
    output_data = output_function(text_input)
    text_input = output_data['Explanation']
    quiz = output_data['Quiz']

    with open(f"data/input_{timestamp}.txt", "w", encoding='utf-8') as f: 
        f.write(text_input)
        f.close()

    run_tts(timestamp, narrator)
    transcription(timestamp)
    json_to_srt(timestamp)
    encode_video(timestamp,video_name=video_source+'.mp4', max_random=video_source_to_max_random[video_source])
    write_quiz(timestamp, quiz)
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
    video_style = request.form.get('video-style')
    video_source = request.form.get('video-source')
    narrator = request.form.get('narrator')
    print(video_style, video_source)

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
        
        generate_url = request.url_root + url_for('generate')

        # Send a POST request to the generate function
        response = requests.post(generate_url, data={'text': text, 'video-style': video_style, 'video-source': video_source, 'narrator': narrator})
        
        # You can handle the response from generate if needed
        if response.status_code == 200:
            return str(response.content.decode('utf-8'))
        else:
            return jsonify({'message': 'Error in generating response', 'details': response.json()}), 500

    return jsonify({'message': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)