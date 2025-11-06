function handleSearch(event, form) {
    const currentInputField = form.querySelector(".search-input");
    const currentInputValue = currentInputField.value.trim();

    if (!currentInputValue) {
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

function initSearchAutocomplete() {
    const searchBoxes = document.querySelectorAll('.search-box');

    searchBoxes.forEach(box => {
        const form = box.querySelector('form');
        const input = form ? form.querySelector('.search-input') : null;
        const ghost = form ? form.querySelector('.ghost-text') : null;
        const suggestionsBox = box.querySelector(".suggestions-box");

        if (!form || !input || !ghost || !suggestionsBox) return;

        // Create a hidden measurement span to calculate prefix width
        const measure = document.createElement('span');
        measure.className = 'measure-span';
        form.appendChild(measure);

        const syncMeasureStyles = () => {
            const cs = window.getComputedStyle(input);
            ["fontFamily","fontSize","fontWeight","letterSpacing","padding"]
                .forEach(prop => measure.style[prop] = cs[prop]);
            ["fontFamily","fontSize","fontWeight","lineHeight"]
                .forEach(prop => ghost.style[prop] = cs[prop]);
            /*measure.style.fontFamily = cs.fontFamily;
            measure.style.fontSize = cs.fontSize;
            measure.style.fontWeight = cs.fontWeight;
            measure.style.letterSpacing = cs.letterSpacing;
            measure.style.padding = cs.padding;
            // Keep ghost visually identical in typography
            ghost.style.fontFamily = cs.fontFamily;
            ghost.style.fontSize = cs.fontSize;
            ghost.style.lineHeight = cs.lineHeight;
            ghost.style.fontWeight = cs.fontWeight;*/
        };
        syncMeasureStyles();

        const updateSuggestions = debounce(async () => {
            const prefix = input.value.trim();
            suggestionsBox.innerHTML = ""; //clear the dropdown

            if (!prefix) {
                ghost.textContent = '';
                ghost.style.paddingLeft = '0px';
                return;
            }
            const allSuggestions = new Set(); // Track suggestions to avoid duplicates
            
            try {
                const res = await fetch(`${window.location.origin}/search_suggest?prefix=${encodeURIComponent(prefix)}`);
                if (!res.ok) return;
                const data = await res.json();
                const first = (data && data.suggestions && data.suggestions[0]) || '';
                if (first.toLowerCase().startsWith(prefix.toLowerCase())){
                    measure.textContent = prefix;
                    const width = measure.getBoundingClientRect().width;
                    ghost.style.paddingLeft = `${width}px`;
                    ghost.textContent = first.slice(prefix.length);
                } else {
                    ghost.textContent = "";
                }
                
                // Collect backend suggestions
                if (data && data.suggestions && Array.isArray(data.suggestions)) {
                    data.suggestions.forEach(suggestion => {
                        allSuggestions.add(suggestion);
                    });
                }
            } catch (_) {
                ghost.textContent = '';
            }
            
            // ✅ Add local dropdown suggestions (if companies exists)
            if (window.companies && Array.isArray(window.companies)) {
                const matches = window.companies
                    .filter(c => c.toLowerCase().includes(prefix.toLowerCase()));
                matches.forEach(match => {
                    allSuggestions.add(match);
                });
            }
            
            // Add all unique suggestions to dropdown (limit to 4) or show "No suggestions available"
            if (allSuggestions.size === 0) {
                const div = document.createElement("div");
                div.classList.add("suggestion-item");
                div.textContent = "No suggestions available";
                div.style.cursor = "default";
                div.style.opacity = "0.6";
                div.onclick = null; // Make it non-clickable
                suggestionsBox.appendChild(div);
            } else {
                Array.from(allSuggestions).slice(0, 4).forEach(suggestion => {
                    const div = document.createElement("div");
                    div.classList.add("suggestion-item");
                    div.textContent = suggestion;
                    div.onclick = () => {
                        input.value = suggestion;
                        ghost.textContent = "";
                        suggestionsBox.innerHTML = "";
                        form.submit();
                    };
                    suggestionsBox.appendChild(div);
                });
            }
        }, 150);

        input.addEventListener('input', updateSuggestions);

        // Accept ghost with Enter and submit immediately
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const remainder = ghost.textContent;
                if (remainder) {
                    e.preventDefault();
                    input.value = input.value.trim() + remainder;
                    ghost.textContent = '';
                    suggestionsBox.innerHTML = "";
                    // Submit the form after accepting completion
                    form.submit();
                }
            }
        });
         // Close dropdown on blur
        input.addEventListener("blur", () => {
            setTimeout(() => suggestionsBox.innerHTML = "", 150);
        });
    });
}

function handleLogin(event) {
    // TODO: Handle client-side validation for login here
}

function handleSignup(event) {
    // TODO: Handle client-side validation for signup here
    //const fullname = document.getElementById('fullname').value;
    //const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        event.preventDefault();
        alert('Passwords do not match!');
        return;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    attachSearchFilterHandler('#searchForm', '.search-filters');
    initSearchAutocomplete();
});