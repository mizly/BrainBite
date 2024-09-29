document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.querySelector("#file-upload input[type=file]");
    const messageDiv = document.getElementById('message');
    const textInput = document.getElementById('text-input');

    document.getElementById('submit-btn').addEventListener('click', async function() {
        const formData = new FormData();
        // Retrieve selected radio button value
        const selectedStyle = document.querySelector('input[name="video-style"]:checked');
        const selectedStyleValue = selectedStyle ? selectedStyle.value : null;
        const selectedVideo = document.querySelector('input[name="video-source"]:checked');
        const selectedVideoValue = selectedVideo ? selectedVideo.value : null;

        //check that text input isn't empty
        if (textInput.value.trim() === '') {
            if (fileInput.files.length === 0) {
                messageDiv.textContent = 'Please choose a file to upload or enter some text.';
                return;
            }
            else {
                formData.append('resume', fileInput.files[0]);
                messageDiv.textContent = 'File submitted successfully!';
            }
        } else {
            // If text input has value, create a Blob and append it as a file
            const textBlob = new Blob([textInput.value.trim()], { type: 'text/plain' });
            formData.append('resume', textBlob, 'alternative.txt'); // Append Blob as 'alternative.txt'
            messageDiv.textContent = 'Text submitted successfully as alternative.txt!';
        }

        // Include the selected video style and video source values
        if (selectedStyleValue) {
            formData.append('video-style', selectedStyleValue);
        }
        
        if (selectedVideoValue) {
            formData.append('video-source', selectedVideoValue);
        }

        try {
            // Send the file to the upload endpoint using Fetch API
            const response = await fetch('/upload-endpoint', {
                method: 'POST',
                body: formData,
            });

            // Check if the upload was successful
            if (response.ok) {
                const timestamp = await response.json(); // Assuming your endpoint returns a JSON with the timestamp
                window.location.href = `/video/${timestamp}`
            } else {
                throw new Error('File upload failed. Make sure the filetype is either pdf, doc, docx, txt and try again.');
            }
        } catch (error) {
            messageDiv.textContent = `Error: ${error.message}`;
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            const fileName = document.querySelector("#file-upload .file-name");
            fileName.textContent = fileInput.files[0].name;
        }
    });
});
