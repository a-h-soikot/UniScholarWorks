// Get toggle options
const toggleOptions = document.querySelectorAll('.toggle-option');
const userTypeInput = document.getElementById('user_type');
const userIdLabel = document.getElementById('userid-label');
const userIdInput = document.getElementById('userid');

// Add click event to toggle options
toggleOptions.forEach(option => {
    option.addEventListener('click', function() {
        // Remove active class from all options
        toggleOptions.forEach(opt => opt.classList.remove('active'));
        
        // Add active class to clicked option
        this.classList.add('active');
        
        // Get user type
        const userType = this.getAttribute('data-user-type');
        
        // Update hidden input
        userTypeInput.value = userType;
        
        // Update label and placeholder based on user type
        if (userType === 'student') {
            userIdLabel.innerHTML = '<i class="fas fa-user-graduate" style="margin-right: 8px;"></i>Student ID';
            userIdInput.placeholder = 'Enter student id or email';
        } else {
            userIdLabel.innerHTML = '<i class="fas fa-chalkboard-teacher" style="margin-right: 8px;"></i>Teacher ID';
            userIdInput.placeholder = 'Enter teacher id or email';
        }
    });
});

const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');

// Add event listener for password toggle
if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', function(e) {
        // Toggle password visibility
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        // Toggle eye icon
        this.querySelector('i').className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
    });
}