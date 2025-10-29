// Mock functionality for navigation and interactions
// TODO: Fix duplicated IDs in the index and search! #searchInput and #suggestions
// TODO: Clean up the code and unnecessary functionality
function handleSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchValue = searchInput.value.trim();

    if (!searchValue) {
        // Prevent form submission
        event.preventDefault();
        alert('Please enter a company name to search');
        return;
    }
}

/**
 * @param {string} formSelector - CSS selector for the search form
 * @param {string} filtersContainerSelector - CSS selector for the filters' container
 * Attaches filter-handling behavior to a given search form.
 * When the form is submitted, this collects all checked filters
 * outside the form (filters sidebar in /search) and adds them as hidden inputs.
 */
function attachSearchFilterHandler(formSelector, filtersContainerSelector) {
    const form = document.querySelector(formSelector);
    const filtersContainer = document.querySelector(filtersContainerSelector);

    if (!form || !filtersContainer) {
        console.warn("Search form or filters container not found.");
        return;
    }

    form.addEventListener('submit', function (e) {
        // Remove previously added hidden inputs
        form.querySelectorAll('input[type="hidden"]').forEach(el => el.remove());

        // Collect all checked filters
        const checkedFilters = filtersContainer.querySelectorAll('input:checked');

        // Add each as hidden input to the form
        checkedFilters.forEach(filter => {
            const hidden = document.createElement('input');
            hidden.type = 'hidden';
            hidden.name = filter.name;
            hidden.value = filter.value;
            form.appendChild(hidden);
        });
    });
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
if (searchInput) {
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
}

// search suggestions end

function performSearch() {
    console.log('Search performed for:', searchInput.value);
    // In a real app, this would trigger API calls
}   //suggestions-block was modified so it also works for this page

function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    console.log('Login attempt:', {email, password});
    alert('Login successful! (This is a mock-up)');
    window.location.href = 'index.html';
}

function handleSignup(event) {
    //const fullname = document.getElementById('fullname').value;
    //const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        event.preventDefault();
        alert('Passwords do not match!');
        return;
    }

    //console.log('Signup attempt:', {fullname, email, password});
    //alert('Account created successfully! (This is a mock-up)');
    //window.location.href = 'login.html';
}

function goToCompany(companyId) {
    console.log('Navigating to company:', companyId);
    window.location.href = 'company.html';
}

// Enter key support for search
document.addEventListener('DOMContentLoaded', () => {
    const searchInputs = document.querySelectorAll('.search-input');
    attachSearchFilterHandler('#searchForm', '.search-filters');
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