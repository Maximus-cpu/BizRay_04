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

function validateEmail(email) {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email);
}

function validatePasswordStrength(password) {
    const errors = [];

    if (password.length < 8) {
        errors.push("Password must be at least 8 characters long");
    }

    if (!/[A-Z]/.test(password)) {
        errors.push("Password must contain at least one uppercase letter");
    }

    if (!/[0-9]/.test(password)) {
        errors.push("Password must contain at least one number");
    }

    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        errors.push("Password must contain at least one special character");
    }

    return errors;
}

// Real-time password strength indicator
function initPasswordStrengthIndicator() {
    const passwordInput = document.getElementById('password');
    if (!passwordInput) return;

    const requirements = {
        length: document.getElementById('req-length'),
        uppercase: document.getElementById('req-uppercase'),
        number: document.getElementById('req-number'),
        special: document.getElementById('req-special')
    };

    passwordInput.addEventListener('input', () => {
        const password = passwordInput.value;

        if (requirements.length) {
            if (password.length >= 8) {
                requirements.length.classList.add('met');
            } else {
                requirements.length.classList.remove('met');
            }
        }

        if (requirements.uppercase) {
            if (/[A-Z]/.test(password)) {
                requirements.uppercase.classList.add('met');
            } else {
                requirements.uppercase.classList.remove('met');
            }
        }

        if (requirements.number) {
            if (/[0-9]/.test(password)) {
                requirements.number.classList.add('met');
            } else {
                requirements.number.classList.remove('met');
            }
        }

        if (requirements.special) {
            if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
                requirements.special.classList.add('met');
            } else {
                requirements.special.classList.remove('met');
            }
        }
    });
}

function handleLogin(event) {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const emailError = document.getElementById('emailError');
    const passwordError = document.getElementById('passwordError');

    let isValid = true;

    // Clear previous errors
    if (emailError) emailError.textContent = '';
    if (passwordError) passwordError.textContent = '';

    // Validate email
    if (!email) {
        if (emailError) emailError.textContent = 'Email is required';
        isValid = false;
    } else if (!validateEmail(email)) {
        if (emailError) emailError.textContent = 'Invalid email format';
        isValid = false;
    }

    // Validate password
    if (!password) {
        if (passwordError) passwordError.textContent = 'Password is required';
        isValid = false;
    }

    if (!isValid) {
        event.preventDefault();
        return false;
    }

    return true;
}

function handleSignup(event) {
    const form = event.target;
    const email = form.querySelector('#email').value.trim();
    const password = form.querySelector('#password').value;
    const confirmPassword = form.querySelector('#confirmPassword').value;

    const emailError = form.querySelector('#emailError');
    const passwordError = form.querySelector('#passwordError');
    const confirmPasswordError = form.querySelector('#confirmPasswordError');

    let isValid = true;

    // clear errors
    [emailError, passwordError, confirmPasswordError].forEach(el => el && (el.textContent = ''));

    if (!email) {
        emailError.textContent = 'Email is required';
        isValid = false;
    } else if (!validateEmail(email)) {
        emailError.textContent = 'Invalid email format';
        isValid = false;
    }

    const passwordErrors = validatePasswordStrength(password);
    if (passwordErrors.length > 0) {
        passwordError.textContent = passwordErrors[0];
        isValid = false;
    }

    if (password !== confirmPassword) {
        confirmPasswordError.textContent = 'Passwords do not match';
        isValid = false;
    }

    if (!isValid) {
        event.preventDefault();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    attachSearchFilterHandler('#searchForm', '.search-filters');
    initGhostAutocomplete();
    initPasswordStrengthIndicator();

    // Attach event listener for client-side validation on signup
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
    }
});