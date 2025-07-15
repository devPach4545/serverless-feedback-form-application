document.addEventListener('DOMContentLoaded', () => {
    
    // Use your deployed API Gateway URL
     const apiUrl = 'https://6xeu6ot0yh.execute-api.us-east-1.amazonaws.com/Prod/feedback/';
    //const apiUrl = 'http://127.0.0.1:3000/feedback';
    
    const form = document.getElementById('feedback-form');
    const responseMessage = document.getElementById('response-message');

    form.addEventListener('submit', async (event) => {
        
        event.preventDefault();

        // Get the form data
        const formData = new FormData(form);
        const data = {
            email: formData.get('email'),
            message: formData.get('message')
        };
        
        // Clear any previous messages
        responseMessage.textContent = '';
        responseMessage.className = '';

        try {
            // Send the data to our backend API
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            // Display success or error message from the server
            if (response.ok) {
                responseMessage.textContent = result.message;
                responseMessage.classList.add('success');
                form.reset(); // Clear the form
            } else {
                responseMessage.textContent = result.error || 'An unknown error occurred.';
                responseMessage.classList.add('error');
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            responseMessage.textContent = 'Failed to connect to the server.';
            responseMessage.classList.add('error');
        }
    });
});