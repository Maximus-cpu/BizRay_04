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
            ["fontFamily", "fontSize", "fontWeight", "letterSpacing", "padding"]
                .forEach(prop => measure.style[prop] = cs[prop]);
            ["fontFamily", "fontSize", "fontWeight", "lineHeight"]
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
                if (first.toLowerCase().startsWith(prefix.toLowerCase())) {
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

            // Add local dropdown suggestions (if companies exists)
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
function initPasswordStrengthIndicator(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    // Locate the requirements elements near the password input
    const requirements = {
        length: input.closest('form').querySelector('#req-length'),
        uppercase: input.closest('form').querySelector('#req-uppercase'),
        number: input.closest('form').querySelector('#req-number'),
        special: input.closest('form').querySelector('#req-special')
    };

    input.addEventListener('input', () => {
        const password = input.value;

        // Length check
        if (requirements.length) {
            password.length >= 8
                ? requirements.length.classList.add('met')
                : requirements.length.classList.remove('met');
        }
        // Uppercase letter check
        if (requirements.uppercase) {
            /[A-Z]/.test(password)
                ? requirements.uppercase.classList.add('met')
                : requirements.uppercase.classList.remove('met');
        }
        // Number check
        if (requirements.number) {
            /[0-9]/.test(password)
                ? requirements.number.classList.add('met')
                : requirements.number.classList.remove('met');
        }
        // Special character check
        if (requirements.special) {
            /[!@#$%^&*(),.?":{}|<>]/.test(password)
                ? requirements.special.classList.add('met')
                : requirements.special.classList.remove('met');
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
    const termsCheckbox = form.querySelector('#termsCheckbox');

    const emailError = form.querySelector('#emailError');
    const passwordError = form.querySelector('#passwordError');
    const confirmPasswordError = form.querySelector('#confirmPasswordError');
    const termsCheckboxError = form.querySelector('#termsCheckboxError');

    let isValid = true;

    // clear errors
    [emailError, passwordError, confirmPasswordError, termsCheckboxError].forEach(el => el && (el.textContent = ''));

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

    if (!termsCheckbox.checked) {
        termsCheckboxError.textContent = 'You must agree to the terms and conditions';
        isValid = false;
    }

    if (!isValid) {
        event.preventDefault();
    }
}

/**
 * Extract financial data from the Financial Overview section and calculate risk indicators.
 * Updates the risk slider widths based on calculated scores.
 */
async function calculateAndUpdateFinancialRiskIndicators() {
    // Check if we're on the company page
    // Find the Financial Overview section specifically by looking for the h2 title
    const financialSections = document.querySelectorAll('.company-page .info-section');
    let financialOverview = null;

    // Find the section with "Financial Overview" title
    for (const section of financialSections) {
        const title = section.querySelector('.section-title');
        if (title && title.textContent.trim() === 'Financial Overview') {
            financialOverview = section.querySelector('.stats-list');
            break;
        }
    }

    const riskList = document.querySelector('.risk-list');

    if (!financialOverview || !riskList) {
        return; // Not on company page or risk list not found
    }

    // Map of label text to API field name
    const labelToFieldMap = {
        'Balance Sheet Total': 'balance_sheet_total',
        'Fixed Assets': 'fixed_assets',
        'Current Assets': 'current_assets',
        'Prepaid Expenses': 'prepaid_expenses',
        'Equity': 'equity',
        'Provisions': 'provisions',
        'Liabilities': 'liabilities',
        'Balance Sheet Profit': 'balance_sheet_profit',
        'Retained Earnings': 'retained_earnings',
        'Current Year Result': 'current_year_result'
    };

    // Extract financial data from DOM
    const financialData = {};
    const statRows = financialOverview.querySelectorAll('.stat-row');

    statRows.forEach(row => {
        const labelElement = row.querySelector('.stat-label');
        const valueElement = row.querySelector('.stat-value');

        if (labelElement && valueElement) {
            const label = labelElement.textContent.trim();
            const value = valueElement.textContent.trim();

            if (labelToFieldMap[label]) {
                financialData[labelToFieldMap[label]] = value;
            }
        }
    });

    // Check if we have any valid data (not all "—")
    const hasData = Object.values(financialData).some(val => val && val !== '—' && val !== '-');

    if (!hasData) {
        // No financial data available, keep sliders at 0%
        console.log('No financial data found');
        return;
    }

    console.log('Financial data extracted:', financialData);

    // Call API to calculate risk indicators
    try {
        const response = await fetch(`${window.location.origin}/api/calculate_financial_risk`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(financialData)
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Failed to calculate financial risk indicators:', response.statusText, errorText);
            return;
        }

        const results = await response.json();
        console.log('Risk results received:', results);

        // Format number with thousand separators
        function formatNumber(num) {
            if (num === null || num === undefined || isNaN(num)) return '—';
            return new Intl.NumberFormat('en-US', {
                minimumFractionDigits: 0,
                maximumFractionDigits: 2
            }).format(num);
        }

        // Format ratio as percentage or decimal
        function formatRatio(value, asPercentage = false) {
            if (value === null || value === undefined || value === 'null' || isNaN(value)) {
                return '—';
            }
            const numValue = typeof value === 'string' ? parseFloat(value) : value;
            if (isNaN(numValue)) return '—';

            if (asPercentage) {
                return (numValue * 100).toFixed(2) + '%';
            }
            return numValue.toFixed(3);
        }

        // Determine color class for number-only indicators based on value and indicator type
        function getValueColorClass(indicator, value, score) {
            if (value === null || value === undefined || isNaN(value)) return '';

            switch (indicator) {
                case 'working_capital':
                    // Positive = good, negative = bad
                    return value > 0 ? 'value-good' : 'value-bad';

                case 'debt_ratio':
                    // Lower is better: <= 0.5 = good, 0.5-1 = warning, > 1 = bad
                    if (value <= 0.5) return 'value-good';
                    if (value <= 1) return 'value-warning';
                    return 'value-bad';

                case 'coverage_fixed_assets':
                    // >= 1 = good, 0.8-1 = warning, < 0.8 = bad
                    if (value >= 1) return 'value-good';
                    if (value >= 0.8) return 'value-warning';
                    return 'value-bad';

                case 'profit_margin':
                    // Positive = good, negative = bad
                    if (value > 0.1) return 'value-good';
                    if (value > 0) return 'value-warning';
                    return 'value-bad';

                default:
                    // Use score as fallback
                    if (score >= 80) return 'value-good';
                    if (score >= 50) return 'value-warning';
                    return 'value-bad';
            }
        }

        // Update all indicators
        const riskList = document.querySelector('.risk-list');
        if (riskList) {
            const riskRows = riskList.querySelectorAll('.stat-row');

            riskRows.forEach(row => {
                const indicator = row.getAttribute('data-indicator');
                if (!indicator) {
                    console.warn('No data-indicator attribute found on row');
                    return;
                }

                if (!results[indicator]) {
                    console.warn(`No result found for indicator: ${indicator}`, results);
                    return;
                }

                const data = results[indicator];
                if (!data) {
                    console.warn(`No data object found for indicator: ${indicator}`);
                    return;
                }

                const score = data.score !== undefined ? data.score : 0;
                const value = data.value !== undefined ? data.value : null;

                console.log(`Processing indicator: ${indicator}, score: ${score}, value: ${value}, data:`, data);

                // Handle slider indicators
                if (row.classList.contains('slider-indicator')) {
                    const sliderFill = row.querySelector('.risk-slider-fill');
                    const sliderValue = row.querySelector('.slider-value');

                    if (sliderFill) {
                        const clampedScore = Math.max(0, Math.min(100, score));
                        sliderFill.style.width = `${clampedScore}%`;

                        // Set color based on score
                        let backgroundColor;
                        if (clampedScore === 100) {
                            backgroundColor = '#43a047'; // Green
                        } else if (clampedScore >= 80) {
                            backgroundColor = '#a8c838'; // Green-Yellow
                        } else if (clampedScore >= 67) {
                            backgroundColor = '#ffa726'; // Orange-Yellow
                        } else if (clampedScore >= 34) {
                            backgroundColor = '#f57c00'; // Orange
                        } else {
                            backgroundColor = '#d32f2f'; // Red
                        }
                        sliderFill.style.backgroundColor = backgroundColor;
                    }

                    if (sliderValue) {
                        // Format ratio values for sliders
                        let formattedValue;
                        if (value === null || value === undefined) {
                            formattedValue = '—';
                        } else {
                            formattedValue = formatRatio(value);
                        }
                        sliderValue.textContent = formattedValue;
                        console.log(`Updated slider value for ${indicator}: ${formattedValue} (raw value: ${value})`);
                    } else {
                        console.warn(`No slider-value element found for ${indicator}`);
                    }
                }

                // Handle number-only indicators
                if (row.classList.contains('number-only')) {
                    const valueElement = row.querySelector('.stat-value-number');

                    if (valueElement) {
                        let displayValue;

                        switch (indicator) {
                            case 'working_capital':
                                // Display as currency-like number
                                displayValue = formatNumber(value);
                                break;

                            case 'debt_ratio':
                            case 'coverage_fixed_assets':
                                // Display as ratio (decimal)
                                displayValue = formatRatio(value, false);
                                break;

                            case 'profit_margin':
                                // Display as percentage
                                displayValue = formatRatio(value, true);
                                break;

                            default:
                                displayValue = formatNumber(value);
                        }

                        valueElement.textContent = displayValue;

                        // Apply color class
                        valueElement.className = 'stat-value-number ' + getValueColorClass(indicator, value, score);
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error calculating financial risk indicators:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    attachSearchFilterHandler('#searchForm', '.search-filters');
    initSearchAutocomplete();
    initPasswordStrengthIndicator('password');
    initPasswordStrengthIndicator('newPassword');

    // Hide Flask flash messages
    document.querySelectorAll('.alert').forEach(alert => {
        // Auto-hide
        const autoHide = setTimeout(() => {
            alert.classList.add('hide');
            setTimeout(() => alert.remove(), 100);
        }, 5000);

        // Dismiss manually
        alert.querySelector('.alert-close').addEventListener('click', () => {
            clearTimeout(autoHide);
            alert.classList.add('hide');
            setTimeout(() => alert.remove(), 100);
        });
    });

    // Attach event listener for client-side validation on signup
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
    }
    // Attach event listener for client-side validation on login
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Calculate and update financial risk indicators on company page
    calculateAndUpdateFinancialRiskIndicators();

    // Also update when financial data might change (e.g., via MutationObserver)
    // This is useful if financial data is loaded dynamically
    const observer = new MutationObserver(() => {
        calculateAndUpdateFinancialRiskIndicators();
    });

    const financialSection = document.querySelector('.company-page .info-section');
    if (financialSection) {
        observer.observe(financialSection, {
            childList: true,
            subtree: true,
            characterData: true
        });
    }
});