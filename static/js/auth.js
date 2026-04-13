// Authentication JavaScript
class AuthSystem {
    constructor() {
        this.apiBase = '/api/v1';
        this.token = localStorage.getItem('authToken');
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuthStatus();
    }

    setupEventListeners() {
        // Login form
        document.getElementById('login-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        // Register form
        document.getElementById('register-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleRegister();
        });
    }

    showTab(tabName) {
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });

        // Remove active class from all nav tabs
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });

        // Show selected tab
        document.getElementById(`${tabName}-tab`).classList.add('active');
        
        // Activate corresponding nav tab
        event.target.classList.add('active');

        // Update footer text
        const footerText = document.getElementById('footer-text');
        if (tabName === 'login') {
            footerText.innerHTML = "Don't have an account? <a href='#' onclick='showTab(\"register\")'>Register here</a>";
        } else {
            footerText.innerHTML = "Already have an account? <a href='#' onclick='showTab(\"login\")'>Login here</a>";
        }
    }

    showAlert(message, type = 'success') {
        const alertEl = document.getElementById('alert');
        alertEl.className = `alert alert-${type}`;
        alertEl.textContent = message;
        alertEl.style.display = 'block';

        // Auto hide after 5 seconds
        setTimeout(() => {
            alertEl.style.display = 'none';
        }, 5000);
    }

    showLoading(show = true) {
        document.getElementById('loading').style.display = show ? 'block' : 'none';
    }

    async handleLogin() {
        const form = document.getElementById('login-form');
        const formData = new FormData(form);
        
        const loginData = {
            email: formData.get('email'),
            password: formData.get('password')
        };

        this.showLoading(true);

        try {
            const response = await fetch(`${this.apiBase}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loginData)
            });

            const data = await response.json();

            if (response.ok) {
                this.token = data.access_token;
                localStorage.setItem('authToken', this.token);
                this.showAlert('Login successful! Redirecting...', 'success');
                
                // Redirect to dashboard after 2 seconds
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 2000);
            } else {
                this.showAlert(data.detail || 'Login failed', 'error');
            }
        } catch (error) {
            this.showAlert('Network error. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async handleRegister() {
        const form = document.getElementById('register-form');
        const formData = new FormData(form);
        
        const password = formData.get('password');
        const confirmPassword = formData.get('confirmPassword');

        // Validate password length
        if (password.length < 8) {
            this.showAlert('Password must be at least 8 characters long', 'error');
            return;
        }

        // Validate passwords match
        if (password !== confirmPassword) {
            this.showAlert('Passwords do not match', 'error');
            return;
        }

        const registerData = {
            username: formData.get('username'),
            email: formData.get('email'),
            password: password
        };

        this.showLoading(true);

        try {
            const response = await fetch(`${this.apiBase}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(registerData)
            });

            const data = await response.json();

            if (response.ok) {
                this.showAlert('Registration successful! Please login.', 'success');
                
                // Clear form and switch to login tab
                form.reset();
                setTimeout(() => {
                    this.showTab('login');
                }, 1500);
            } else {
                this.showAlert(data.detail || 'Registration failed', 'error');
            }
        } catch (error) {
            this.showAlert('Network error. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async checkAuthStatus() {
        if (this.token) {
            try {
                const response = await fetch(`${this.apiBase}/me`, {
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    }
                });

                if (response.ok) {
                    // User is authenticated, redirect to dashboard
                    window.location.href = '/dashboard';
                } else {
                    // Token is invalid, remove it
                    localStorage.removeItem('authToken');
                    this.token = null;
                }
            } catch (error) {
                localStorage.removeItem('authToken');
                this.token = null;
            }
        }
    }

    logout() {
        localStorage.removeItem('authToken');
        this.token = null;
        window.location.href = '/';
    }
}

// Password strength checker
function checkPasswordStrength(password) {
    const strengthBar = document.getElementById('strength-bar');
    const strengthText = document.getElementById('strength-text');
    const passwordStrength = document.getElementById('password-strength');
    const requirements = document.getElementById('password-requirements');
    
    if (password.length === 0) {
        passwordStrength.style.display = 'none';
        requirements.style.color = '#666';
        return;
    }
    
    passwordStrength.style.display = 'block';
    
    let strength = 0;
    let feedback = '';
    
    // Length check
    if (password.length >= 8) {
        strength += 25;
        requirements.style.color = '#28a745';
    } else {
        requirements.style.color = '#dc3545';
        feedback = 'Too short (min 8 chars)';
    }
    
    // Additional strength checks
    if (password.length >= 12) strength += 25;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 25;
    if (/[0-9]/.test(password)) strength += 12.5;
    if (/[^a-zA-Z0-9]/.test(password)) strength += 12.5;
    
    // Update strength bar
    strengthBar.style.width = strength + '%';
    
    // Update strength text and color
    if (strength <= 25) {
        strengthBar.style.background = '#dc3545';
        strengthText.textContent = feedback || 'Weak';
        strengthText.style.color = '#dc3545';
    } else if (strength <= 50) {
        strengthBar.style.background = '#ffc107';
        strengthText.textContent = 'Fair';
        strengthText.style.color = '#ffc107';
    } else if (strength <= 75) {
        strengthBar.style.background = '#17a2b8';
        strengthText.textContent = 'Good';
        strengthText.style.color = '#17a2b8';
    } else {
        strengthBar.style.background = '#28a745';
        strengthText.textContent = 'Strong';
        strengthText.style.color = '#28a745';
    }
}

// Global function for tab switching
function showTab(tabName) {
    authSystem.showTab(tabName);
}

// Initialize the auth system
const authSystem = new AuthSystem();
