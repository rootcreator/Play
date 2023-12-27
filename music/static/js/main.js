document.addEventListener('DOMContentLoaded', function() {
    // Your JavaScript logic here

    // Example: Fetching data using AJAX
    // Replace 'url' with your actual endpoint
    fetch('templates/index.html')
        .then(response => response.json())
        .then(data => {
            // Handle the fetched data
            console.log(data);

            // Modify the DOM based on the fetched data
            const contentArea = document.getElementById('content-area');
            if (contentArea) {
                contentArea.innerHTML = '<h3>Fetched Data</h3>';
                // You can create and append elements dynamically here
            }
        })
        .catch(error => {
            // Handle errors during data fetching
            console.error('Error fetching data:', error);
        });

    // Add event listeners or other logic to handle user interactions, etc.
    // Example: Handle a click event
    const button = document.getElementById('my-button');
    if (button) {
        button.addEventListener('click', function(event) {
            // Perform actions on button click
            console.log('Button clicked!');
        });
    }
});
