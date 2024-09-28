import requests

# Define the URL of your Flask API endpoint
url = 'https://6cc2-174-89-15-216.ngrok-free.app/generate'

# Create the payload with the text input
payload = {
    "text": "Hello, this is a test video!"
}

# Set the custom header
headers = {
    "ngrok-skip-browser-warning": "true"  # or any value you want
}

# Send a POST request to the API with the custom header
response = requests.post(url, json=payload, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Save the received video file
    with open('output.mp4', 'wb') as f:
        f.write(response.content)
    print("Video received and saved as 'output.mp4'.")
else:
    print(f"Failed to receive video: {response.status_code} - {response.text}")
