document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.querySelector("#file-upload input[type=file]");
    const messageDiv = document.getElementById('message');

    document.getElementById('submit-btn').addEventListener('click', async function() {
        // Check if a file is selected
        if (fileInput.files.length === 0) {
            messageDiv.textContent = 'Please choose a file to upload.';
            return;
        }

        // Create FormData object to prepare the file for submission
        const formData = new FormData();
        formData.append('resume', fileInput.files[0]);

        try {
            // Send the file to the upload endpoint using Fetch API
            const response = await fetch('/upload-endpoint', {
                method: 'POST',
                body: formData,
            });

            // Check if the upload was successful
            if (response.ok) {
                const result = await response.json(); // Assuming the server responds with JSON
                messageDiv.textContent = `File uploaded successfully! ${result.message}`;
            } else {
                throw new Error('File upload failed');
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
