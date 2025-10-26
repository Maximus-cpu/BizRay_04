// Mock functionality for navigation and interactions

function handleSearch() {
    const searchInput = document.getElementById('homeSearch');
    if (searchInput && searchInput.value.trim()) {
        window.location.href = 'search.html';
    }
}

function performSearch() {
    console.log('Search performed');
    // In a real app, this would trigger API calls
}

function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    console.log('Login attempt:', { email, password });
    alert('Login successful! (This is a mock-up)');
    window.location.href = 'index.html';
}

function handleSignup(event) {
    event.preventDefault();
    const fullname = document.getElementById('fullname').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }
    
    console.log('Signup attempt:', { fullname, email, password });
    alert('Account created successfully! (This is a mock-up)');
    window.location.href = 'login.html';
}

function goToCompany(companyId) {
    console.log('Navigating to company:', companyId);
    window.location.href = 'company.html';
}

// Enter key support for search
document.addEventListener('DOMContentLoaded', () => {
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                if (input.id === 'homeSearch') {
                    handleSearch();
                } else {
                    performSearch();
                }
            }
        });
    });
});