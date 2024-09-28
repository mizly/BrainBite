import requests
import sys
import json
from tts import main
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def run_tts(voice='en_us_001'):
    session_id = os.getenv('TIKTOK_SESSION_ID')
    if not session_id:
        raise ValueError("TIKTOK_SESSION_ID environment variable is not set")
    
    sys.argv = ['main.py', '-v', voice, '-f', 'input.txt', '--session', 'cd8262ea78f5546c3c4a103dec990db9']
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

def json_to_srt(json_data):
    srt_content = []
    subtitle_index = 1

    for word_info in json_data['words']:
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
    with open("output.srt", "w", encoding="utf-8") as f:
        f.write("\n".join(srt_content))
        f.close()


run_tts()