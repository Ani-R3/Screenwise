class ScreenwiseAuth {
    constructor() {
        this.isSignUpMode = false;
        this.initializeElements();
        this.bindEvents();
        this.updateFormValidation();
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

        // Social buttons
        this.googleLoginBtn = document.getElementById('googleLoginBtn');
        this.xLoginBtn = document.getElementById('xLoginBtn');
        this.googleSignUpBtn = document.getElementById('googleSignUpBtn');
        this.xSignUpBtn = document.getElementById('xSignUpBtn');
    }

    bindEvents() {
        // Toggle between login and signup
        this.toggleBtn.addEventListener('click', () => this.toggleForms());

        // Form submissions
        //this.loginFormElement.addEventListener('submit', (e) => this.handleLogin(e));
        //this.signUpFormElement.addEventListener('submit', (e) => this.handleSignUp(e));

        // Input validation
        this.loginEmail.addEventListener('input', () => this.validateLoginForm());
        this.loginPassword.addEventListener('input', () => this.validateLoginForm());
        this.signUpEmail.addEventListener('input', () => this.validateSignUpForm());
        this.signUpPassword.addEventListener('input', () => this.validateSignUpForm());
        this.signUpConfirmPassword.addEventListener('input', () => this.validateSignUpForm());

        // Keyboard navigation
        this.addKeyboardNavigation();

        // Social login buttons
        this.googleLoginBtn.addEventListener('click', () => this.handleGoogleLogin());
        this.xLoginBtn.addEventListener('click', () => this.handleXLogin());
        this.googleSignUpBtn.addEventListener('click', () => this.handleGoogleLogin());
        this.xSignUpBtn.addEventListener('click', () => this.handleXLogin());
    }

    addKeyboardNavigation() {
        /*
        // Login form keyboard navigation
        this.loginPassword.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && this.isLoginFormValid()) {
                this.handleLogin(e);
            }
        });

        // Sign up form keyboard navigation
        this.signUpConfirmPassword.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && this.isSignUpFormValid()) {
                this.handleSignUp(e);
            }
        });
        */

        // Toggle form with keyboard
        this.toggleBtn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.toggleForms();
            }
        });
    }

    toggleForms() {
        this.isSignUpMode = !this.isSignUpMode;
        
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
        
        this.clearForms();
    }

    clearForms() {
        // Clear login form
        this.loginEmail.value = '';
        this.loginPassword.value = '';
        
        // Clear signup form
        this.signUpEmail.value = '';
        this.signUpPassword.value = '';
        this.signUpConfirmPassword.value = '';
        
        // Reset validation
        this.validateLoginForm();
        this.validateSignUpForm();
        this.hidePasswordError();
    }

    validateLoginForm() {
        const isValid = this.isLoginFormValid();
        this.loginBtn.disabled = !isValid;
    }

    validateSignUpForm() {
        const isValid = this.isSignUpFormValid();
        this.signUpBtn.disabled = !isValid;
        
        // Check password match
        if (this.signUpConfirmPassword.value && !this.passwordsMatch()) {
            this.showPasswordError();
            this.signUpConfirmPassword.classList.add('error');
        } else {
            this.hidePasswordError();
            this.signUpConfirmPassword.classList.remove('error');
        }
    }

    isLoginFormValid() {
        return this.loginEmail.value.trim() && this.loginPassword.value.trim();
    }

    isSignUpFormValid() {
        return this.signUpEmail.value.trim() && 
               this.signUpPassword.value.trim() && 
               this.signUpConfirmPassword.value.trim() && 
               this.passwordsMatch();
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
/*
    handleLogin(event) {
        event.preventDefault();
        
        if (!this.isLoginFormValid()) {
            return;
        }

        const email = this.loginEmail.value.trim();
        const password = this.loginPassword.value.trim();
        
        console.log('Login attempt:', { email });
        
        // Here you would typically make an API call to your authentication service
        alert(`Login attempt for: ${email}`);
    }

    handleSignUp(event) {
        event.preventDefault();
        
        if (!this.isSignUpFormValid()) {
            return;
        }

        const email = this.signUpEmail.value.trim();
        const password = this.signUpPassword.value.trim();
        
        console.log('Sign up attempt:', { email });
        
        // Here you would typically make an API call to your authentication service
        alert(`Sign up attempt for: ${email}`);
    }
*/
    handleGoogleLogin() {
        console.log('Google login clicked');
        
        // Here you would integrate with Google OAuth
        // Example: window.location.href = '/auth/google';
        alert('Google login would be initiated here');
    }

    handleXLogin() {
        console.log('X (Twitter) login clicked');
        
        // Here you would integrate with X OAuth
        // Example: window.location.href = '/auth/twitter';
        alert('X login would be initiated here');
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ScreenwiseAuth();
});