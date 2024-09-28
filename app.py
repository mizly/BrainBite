import requests
import sys
import json
from tts import main
import os
from dotenv import load_dotenv
import subprocess
import random
import time
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

def run_tts(voice='en_us_001'):
    session_id = os.getenv('TIKTOK_SESSION_ID')
    if not session_id:
        raise ValueError("TIKTOK_SESSION_ID environment variable is not set")
    
    sys.argv = ['main.py', '-v', voice, '-f', 'input.txt', '--session', session_id]
    main()

def transcription():
    url = "http://localhost:8765/transcriptions?async=false"
    files = {
        "audio": open("voice.mp3", "rb"),
        "transcript": open("input.txt", "rb")
    }

    response = requests.post(url, files=files)

    # Print the response from the server
    print(response.status_code)

    if response.status_code == 200:
        #save the response to a file
        with open("transcription.json", "w") as f:
            f.write(response.text)
            f.close()

def json_to_srt():
    json_data = json.load(open("transcription.json"))
    srt_content = []
    subtitle_index = 1

    for word_info in json_data['words']:
        if word_info.get('case') != 'success':
            continue
        print("current word info: ", word_info)
        start_time = word_info['start']
        end_time = word_info['end']
        word = word_info['word']

        # Convert seconds to SRT time format (HH:MM:SS,ms)
        def convert_time(seconds):
            ms = int((seconds % 1) * 1000)
            s = int(seconds)
            hrs = s // 3600
            mins = (s % 3600) // 60
            secs = s % 60
            return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

        start_str = convert_time(start_time)
        end_str = convert_time(end_time)

        # Append the index, timing, and text to the SRT content
        srt_content.append(f"{subtitle_index}")
        srt_content.append(f"{start_str} --> {end_str}")
        srt_content.append(word)
        srt_content.append("")  # Empty line for separation

        subtitle_index += 1

    #write the srt content to a file
    with open("transcription.srt", "w", encoding="utf-8") as f:
        f.write("\n".join(srt_content))
        f.close()

def encode_video(video_name='subway.mp4'):
    start_time = random.randint(0, 1800)
    command = (
    f"ffmpeg -ss {start_time} -i gameplay/{video_name} -i voice.mp3 -vf subtitles=transcription.srt "
    f"-c:v libx264 -c:a libmp3lame -map 0:v:0 -map 1:a:0 -shortest -y static/output.mp4"
)
    # Run the command
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

'''
run_tts("en_male_funny")
transcription()
json_to_srt()
encode_video()
'''

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/generate', methods=['POST'])
def generate():
    text_input = request.form['text']
    timestamp = int(time.time())
    unique_filename = f"{timestamp}"

    with open("input.txt", "w") as f:
        f.write(text_input)
        f.close()

    voice = 'en_us_001'
    run_tts(voice)
    transcription()
    json_to_srt()
    encode_video()
    return render_template('video.html')

if __name__ == '__main__':
    app.run(debug=True)