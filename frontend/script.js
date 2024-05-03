document.addEventListener('DOMContentLoaded', function () {
    // Handle PDF form submission
    document.getElementById('pdfForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const messageElement = document.getElementById('message');
        const backendBaseUrl = 'http://localhost:3001';

        if (formData.get('pdf')) {
            fetch(`${backendBaseUrl}/upload-pdf`, {
                method: 'POST',
                body: formData,
            })
            .then(response => responseHandler(response, messageElement))
            .catch((error) => errorHandler(error, messageElement));
        } else {
            messageElement.textContent = 'Please select a PDF file to upload.';
        }
    });

    // Handle URL form submission
    document.getElementById('urlForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const messageElement = document.getElementById('message');
        const backendBaseUrl = 'http://localhost:3001';

        if (formData.get('url')) {
            fetch(`${backendBaseUrl}/submit-url`, {
                method: 'POST',
                body: formData,
            })
            .then(response => responseHandler(response, messageElement))
            .catch((error) => errorHandler(error, messageElement));
        } else {
            messageElement.textContent = 'Please enter a URL.';
        }
    });
});

function responseHandler(response, messageElement) {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.text().then(data => {
        messageElement.textContent = data;
    });
}

function errorHandler(error, messageElement) {
    console.error('Error:', error);
    messageElement.textContent = 'Failed to process your request.';
}
