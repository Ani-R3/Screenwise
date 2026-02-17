class ScreenwiseAuth {
    constructor() {
        this.isSignUpMode = false;
        this.initializeElements();
        this.bindEvents();
        // Check context for errors and switch to signup mode if needed (for server-side errors)
        this.checkInitialMode(); 
    }

    initializeElements() {
        // Forms
        this.loginForm = document.getElementById('loginForm');
        this.signUpForm = document.getElementById('signUpForm');
        this.loginFormElement = document.getElementById('loginFormElement');
        this.signUpFormElement = document.getElementById('signUpFormElement');

        // Buttons
        this.toggleBtn = document.getElementById('toggleBtn');
        this.loginBtn = document.getElementById('loginBtn');
        this.signUpBtn = document.getElementById('signUpBtn');

        // Inputs
        this.loginEmail = document.getElementById('login-email');
        this.loginPassword = document.getElementById('login-password');
        this.signUpEmail = document.getElementById('signup-email');
        this.signUpPassword = document.getElementById('signup-password');
        this.signUpConfirmPassword = document.getElementById('signup-confirm-password');

        // Messages
        this.toggleMessage = document.getElementById('toggleMessage');
        this.passwordError = document.getElementById('passwordError');
        
        // Ensure all buttons are enabled by default for Django submission (we rely on the 'required' HTML attribute)
        this.signUpBtn.removeAttribute('disabled');
    }

    bindEvents() {
        // Toggle between login and signup
        this.toggleBtn.addEventListener('click', () => this.toggleForms());

        // Input validation (only used for password match visual error now)
        this.signUpPassword.addEventListener('input', () => this.validateSignUpForm());
        this.signUpConfirmPassword.addEventListener('input', () => this.validateSignUpForm());
        
        // We removed all explicit form.addEventListener('submit') calls and manual 
        // login/signup validation to let the native HTML form submit to Django.
    }

    ccheckInitialMode() {
        // 🚨 REPLACE the old checkInitialMode with this: 🚨
        const body = document.querySelector('body');
        if (body.dataset.signupError === 'true') {
            this.isSignUpMode = true;
        }

        // This will now correctly show the signup form if 'isSignUpMode' was set to true
        this.toggleForms(false); // Do not clear forms on initial load
    }

    
    toggleForms(shouldClear = true) {
        if (shouldClear) {
             this.isSignUpMode = !this.isSignUpMode;
        }

        if (this.isSignUpMode) {
            this.loginForm.style.display = 'none';
            this.signUpForm.style.display = 'block';
            this.toggleMessage.textContent = 'Have an account? ';
            this.toggleBtn.textContent = 'Log in';
        } else {
            this.loginForm.style.display = 'block';
            this.signUpForm.style.display = 'none';
            this.toggleMessage.textContent = "Don't have an account? ";
            this.toggleBtn.textContent = 'Sign up';
        }
        
        if (shouldClear) {
            this.clearForms();
        }
    }

    clearForms() {
        // Clear inputs
        this.loginEmail.value = '';
        this.loginPassword.value = '';
        this.signUpEmail.value = '';
        this.signUpPassword.value = '';
        this.signUpConfirmPassword.value = '';
        
        // Reset validation display
        this.hidePasswordError();
    }

    // Only validation logic remaining is for password match visual feedback
    validateSignUpForm() {
        if (this.signUpConfirmPassword.value && !this.passwordsMatch()) {
            this.showPasswordError();
        } else {
            this.hidePasswordError();
        }
    }

    passwordsMatch() {
        return this.signUpPassword.value === this.signUpConfirmPassword.value;
    }

    showPasswordError() {
        this.passwordError.style.display = 'block';
    }

    hidePasswordError() {
        this.passwordError.style.display = 'none';
    }

    // Removed all handleLogin/handleSignUp methods to rely on native form submission.

    handleGoogleLogin() {
        alert('Google login would be initiated here');
    }

    handleXLogin() {
        alert('X login would be initiated here');
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ScreenwiseAuth();
});
