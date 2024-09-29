import requests
import sys
import json
from tts import main
import os
import subprocess
import random

def run_tts(timestamp, voice='en_us_001'):
    session_id = os.environ.get('TIKTOK_SESSION_ID')
    if not session_id:
        raise ValueError("TIKTOK_SESSION_ID environment variable is not set")
    
    sys.argv = ['main.py', '-v', voice, '-f', f'data/input_{timestamp}.txt', '--session', session_id]
    main(timestamp)
    #rename the output file from voice.mp3 to voice_{timestamp}.mp3
    os.rename(f"voice.mp3", f"data/voice_{timestamp}.mp3")

def transcription(timestamp):
    url = "http://localhost:8765/transcriptions?async=false"
    files = {
        "audio": open(f"data/voice_{timestamp}.mp3", "rb"),
        "transcript": open(f"data/input_{timestamp}.txt", "rb")
    }

    response = requests.post(url, files=files)

    # Print the response from the server
    print(response.status_code)

    if response.status_code == 200:
        #save the response to a file
        with open(f"data/transcription_{timestamp}.json", "w") as f:
            f.write(response.text)
            f.close()

def json_to_srt(timestamp):
    json_data = json.load(open(f"data/transcription_{timestamp}.json"))
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
    with open(f"data/transcription_{timestamp}.srt", "w", encoding="utf-8") as f:
        f.write("\n".join(srt_content))
        f.close()

def encode_video(timestamp, video_name='subway.mp4', max_random=1800):
    start_time = random.randint(0, max_random)
    command = (
    f"ffmpeg -ss {start_time} -i gameplay/{video_name} -i data/voice_{timestamp}.mp3 -vf \"subtitles=data/transcription_{timestamp}.srt:force_style='Alignment=10'\" "
    f"-c:v libx264 -c:a aac -map 0:v:0 -map 1:a:0 -shortest -y static/videos/output_{timestamp}.mp4"
    )
    # Run the command
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def write_quiz(timestamp, quiz):
    with open(f"static/videos/quiz_{timestamp}.json", "w") as f:
        json.dump(quiz, f)
        f.close()
