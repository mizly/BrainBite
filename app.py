import time
from flask import Flask, request, render_template
from generate_video import *
from pypdf import PdfReader

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

if __name__ == '__main__':
    app.run(debug=True)