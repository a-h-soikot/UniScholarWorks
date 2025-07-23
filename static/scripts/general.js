// Handle flash message closing
// Find all close buttons in flash messages
const closeButtons = document.querySelectorAll('.flash-message .flash-close');

// Add click event to each close button
closeButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Find the parent flash message and remove it
        const flashMessage = button.closest('.flash-message');
        if (flashMessage) {
            flashMessage.style.opacity = '0';
            setTimeout(() => {
                flashMessage.remove();
            }, 300); // Delay before removing the element in milliseconds
        }
    });
});

// Auto-hide flash messages after some seconds
const flashMessages = document.querySelectorAll('.flash-message');
flashMessages.forEach(message => {
    setTimeout(() => {
        message.style.opacity = '0';
        setTimeout(() => {
            message.remove();
        }, 300);
    }, 15000); // Set timeout in milliseconds
});
