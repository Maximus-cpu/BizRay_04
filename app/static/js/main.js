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

// Inline autocomplete (ghost completion) using backend suggestions
function debounce(fn, delay) {
    let t;
    return function (...args) {
        clearTimeout(t);
        t = setTimeout(() => fn.apply(this, args), delay);
    }
}

function initGhostAutocomplete() {
    const searchBoxes = document.querySelectorAll('.search-box');
    searchBoxes.forEach(box => {
        const form = box.querySelector('form');
        if (!form) return;
        const input = form.querySelector('.search-input');
        const ghost = form.querySelector('.ghost-text');
        if (!input || !ghost) return;

        // Create a hidden measurement span to calculate prefix width
        const measure = document.createElement('span');
        measure.className = 'measure-span';
        form.appendChild(measure);

        const syncMeasureStyles = () => {
            const cs = window.getComputedStyle(input);
            measure.style.fontFamily = cs.fontFamily;
            measure.style.fontSize = cs.fontSize;
            measure.style.fontWeight = cs.fontWeight;
            measure.style.letterSpacing = cs.letterSpacing;
            measure.style.padding = cs.padding;
            // Keep ghost visually identical in typography
            ghost.style.fontFamily = cs.fontFamily;
            ghost.style.fontSize = cs.fontSize;
            ghost.style.lineHeight = cs.lineHeight;
            ghost.style.fontWeight = cs.fontWeight;
        };
        syncMeasureStyles();

        const updateGhost = debounce(async () => {
            const prefix = input.value.trim();
            if (!prefix) {
                ghost.textContent = '';
                ghost.style.paddingLeft = '0px';
                return;
            }
            try {
                const res = await fetch(`${window.location.origin}/search_suggest?prefix=${encodeURIComponent(prefix)}`);
                if (!res.ok) return;
                const data = await res.json();
                const first = (data && data.suggestions && data.suggestions[0]) || '';
                if (!first) {
                    ghost.textContent = '';
                    ghost.style.paddingLeft = '0px';
                    return;
                }
                // Only show if suggestion starts with current input (case-insensitive)
                const starts = first.toLowerCase().startsWith(prefix.toLowerCase());
                if (!starts) {
                    ghost.textContent = '';
                    ghost.style.paddingLeft = '0px';
                    return;
                }

                // Compute width of current typed prefix and position remainder after it
                syncMeasureStyles();
                measure.textContent = prefix;
                const prefixWidth = measure.getBoundingClientRect().width;
                const remainder = first.slice(prefix.length);
                ghost.textContent = remainder;
                ghost.style.paddingLeft = `${prefixWidth}px`;
            } catch (_) {
                ghost.textContent = '';
                ghost.style.paddingLeft = '0px';
            }
        }, 150);

        input.addEventListener('input', updateGhost);

        // Accept ghost with Enter and submit immediately
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const suggestionRemainder = ghost.textContent || '';
                if (suggestionRemainder) {
                    e.preventDefault();
                    input.value = input.value.trim() + suggestionRemainder;
                    ghost.textContent = '';
                    ghost.style.paddingLeft = '0px';
                    // Submit the form after accepting completion
                    form.submit();
                }
            }
        });
    });
}

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
    attachSearchFilterHandler('#searchForm', '.search-filters');
    initGhostAutocomplete();
});