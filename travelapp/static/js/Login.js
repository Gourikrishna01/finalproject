// Login.js

document.addEventListener('DOMContentLoaded', function () {
    // Function to validate the username
    function validateUsername() {
        var usernameInput = document.getElementsByName('username')[0];
        var usernameValue = usernameInput.value.trim();

        // Check if the username meets the criteria
        var usernameRegex = /^(?=.*[A-Za-z0-9])[A-Za-z0-9]{6,}$/;
        if (!usernameRegex.test(usernameValue)) {
            alert('Username must be at least 6 characters long and contain only alphanumeric characters.');
            return false;
        }

        return true;
    }

    // Function to validate the password
    function validatePassword() {
        var passwordInput = document.getElementsByName('password')[0];
        var passwordValue = passwordInput.value.trim();

        // Check if the password meets the criteria
        var passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&*!])[A-Za-z\d@#$%^&*!]{8,}$/;
        if (!passwordRegex.test(passwordValue)) {
            alert('Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one special character, and one number.');
            return false;
        }

        return true;
    }

    // Function to handle form submission
    function handleSubmit(event) {
        // Validate username and password before submitting the form
        if (!validateUsername() || !validatePassword()) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    }

    // Attach the validation functions to the form submission event
    var loginForm = document.querySelector('form');
    loginForm.addEventListener('submit', handleSubmit);
});
