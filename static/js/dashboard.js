// Dashboard JavaScript
class Dashboard {
    constructor() {
        this.apiBase = '/api/v1';
        this.token = localStorage.getItem('authToken');
        this.init();
    }

    init() {
        this.checkAuth();
        this.loadUserData();
    }

    async checkAuth() {
        if (!this.token) {
            window.location.href = '/';
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/me`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (!response.ok) {
                throw new Error('Token invalid');
            }
        } catch (error) {
            console.error('Auth check failed:', error);
            localStorage.removeItem('authToken');
            window.location.href = '/';
        }
    }

    async loadUserData() {
        try {
            const response = await fetch(`${this.apiBase}/me`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const userData = await response.json();
                this.displayUserData(userData);
            } else {
                throw new Error('Failed to load user data');
            }
        } catch (error) {
            console.error('Error loading user data:', error);
            this.showAlert('Failed to load user data', 'error');
        }
    }

    displayUserData(user) {
        document.getElementById('user-id').textContent = user.id;
        document.getElementById('user-username').textContent = user.username;
        document.getElementById('user-email').textContent = user.email;
        document.getElementById('user-status').textContent = user.is_active ? 'Active' : 'Inactive';
        document.getElementById('user-created').textContent = new Date(user.created_at).toLocaleDateString();
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

    logout() {
        localStorage.removeItem('authToken');
        window.location.href = '/';
    }
}

// Global functions
function refreshUserData() {
    dashboard.loadUserData();
    dashboard.showAlert('User data refreshed', 'success');
}

function logout() {
    dashboard.logout();
}

function showToken() {
    const tokenDisplay = document.getElementById('token-display');
    const jwtToken = document.getElementById('jwt-token');
    
    tokenDisplay.style.display = 'block';
    jwtToken.textContent = dashboard.token || 'No token found';
}

function hideToken() {
    const tokenDisplay = document.getElementById('token-display');
    tokenDisplay.style.display = 'none';
}

function copyToken() {
    const token = dashboard.token;
    if (token) {
        navigator.clipboard.writeText(token).then(() => {
            dashboard.showAlert('Token copied to clipboard!', 'success');
        }).catch(() => {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = token;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            dashboard.showAlert('Token copied to clipboard!', 'success');
        });
    } else {
        dashboard.showAlert('No token to copy', 'error');
    }
}

// Initialize dashboard
const dashboard = new Dashboard();
