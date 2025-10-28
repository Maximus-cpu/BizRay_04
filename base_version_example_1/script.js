// Mock functionality for navigation and interactions

function handleSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput && searchInput.value.trim()) {
        window.location.href = 'search.html';
    }
}
//The following 60 lines are for the search suggestions

// Mock company data    (for the search suggestions on the index.html
const companies = [
    "OpenAI",
    "Google",
    "Microsoft",
    "Amazon",
    "Apple",
    "Nvidia",
    "Meta",
    "IBM",
    "Intel",
    "Tesla",
    "Samsung",
    "Oracle",
    "Adobe"
];

//handling search input
const searchInput = document.getElementById("searchInput");
const suggestionsBox = document.getElementById("suggestions");

// Listen for typing
searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase().trim();
    suggestionsBox.innerHTML = "";

    if (!query) {   // if there is no text, stop and do nothing
        suggestionsBox.innerHTML = '';
        suggestionsBox.style.display = 'none';
        return; // Stop the function early
    }

    // filtering through the data, for things that match the input
    const filtered = companies
        .filter((company) => company.toLowerCase().includes(query))
        .slice(0, 4);// max of 4 suggestions

    filtered.forEach((name) => {
        const div = document.createElement("div");
        div.classList.add("suggestion-item");
        div.textContent = name;
        div.addEventListener("click", () => {
            searchInput.value = name;
            suggestionsBox.innerHTML = "";
        });
        suggestionsBox.appendChild(div);
    });
});

    // Hide suggestions when clicking outside of the box
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".search-box")) {
            suggestionsBox.innerHTML = "";
        }
    });
// search suggestions end

function performSearch() {
    console.log('Search performed for:', searchInput.value);
    // In a real app, this would trigger API calls
}   //suggestions-block was modified so it also works for this page

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