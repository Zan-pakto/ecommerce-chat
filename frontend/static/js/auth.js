// Authentication state
let currentUser = null;
let accessToken = localStorage.getItem('accessToken');

// DOM Elements
const authButtons = document.getElementById('authButtons');
const userInfo = document.getElementById('userInfo');
const usernameSpan = document.getElementById('username');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');

// Initialize authentication state
function initAuth() {
    if (accessToken) {
        fetchUserProfile();
    } else {
        showAuthButtons();
    }
}

// Show login modal
function showLoginModal() {
    const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
    loginModal.show();
}

// Show register modal
function showRegisterModal() {
    const registerModal = new bootstrap.Modal(document.getElementById('registerModal'));
    registerModal.show();
}

// Handle login form submission
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(loginForm);
    
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: formData.get('username'),
                password: formData.get('password')
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            accessToken = data.access_token;
            localStorage.setItem('accessToken', accessToken);
            currentUser = data.user;
            showUserInfo();
            bootstrap.Modal.getInstance(document.getElementById('loginModal')).hide();
            loginForm.reset();
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('An error occurred during login');
    }
});

// Handle register form submission
registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(registerForm);
    
    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: formData.get('username'),
                email: formData.get('email'),
                password: formData.get('password')
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('registerModal')).hide();
            registerForm.reset();
            showSuccess('Registration successful! Please login.');
            showLoginModal();
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('An error occurred during registration');
    }
});

// Fetch user profile
async function fetchUserProfile() {
    try {
        const response = await fetch('/api/auth/profile', {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            currentUser = data;
            showUserInfo();
        } else {
            logout();
        }
    } catch (error) {
        logout();
    }
}

// Show user info
function showUserInfo() {
    authButtons.classList.add('d-none');
    userInfo.classList.remove('d-none');
    usernameSpan.textContent = currentUser.username;
}

// Show auth buttons
function showAuthButtons() {
    authButtons.classList.remove('d-none');
    userInfo.classList.add('d-none');
}

// Logout
function logout() {
    accessToken = null;
    currentUser = null;
    localStorage.removeItem('accessToken');
    showAuthButtons();
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.querySelector('.modal-body').prepend(errorDiv);
    setTimeout(() => errorDiv.remove(), 5000);
}

// Show success message
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    document.querySelector('.container').prepend(successDiv);
    setTimeout(() => successDiv.remove(), 5000);
}

// Initialize auth on page load
document.addEventListener('DOMContentLoaded', initAuth); 