// Main JavaScript for Student Risk Prediction System
// Handles form validation, interactions, and UI enhancements

document.addEventListener('DOMContentLoaded', function() {
    
    // ══════════════════════════════════════════════════════════════
    // FORM VALIDATION
    // ══════════════════════════════════════════════════════════════
    
    const predictionForm = document.getElementById('predictionForm');
    
    if (predictionForm) {
        // Real-time validation
        const inputs = predictionForm.querySelectorAll('input, select');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('invalid')) {
                    validateField(this);
                }
            });
        });
        
        // Form submission
        predictionForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (isValid) {
                showLoadingState();
            } else {
                e.preventDefault();
                showValidationError();
            }
        });
    }
    
    function validateField(field) {
        const value = field.value.trim();
        const fieldType = field.type;
        const fieldName = field.name;
        let isValid = true;
        let errorMessage = '';
        
        // Required check
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'This field is required';
        }
        
        // Number validation
        if (fieldType === 'number' && value) {
            const num = parseFloat(value);
            const min = parseFloat(field.min);
            const max = parseFloat(field.max);
            
            if (isNaN(num)) {
                isValid = false;
                errorMessage = 'Please enter a valid number';
            } else if (min !== undefined && num < min) {
                isValid = false;
                errorMessage = `Value must be at least ${min}`;
            } else if (max !== undefined && num > max) {
                isValid = false;
                errorMessage = `Value must not exceed ${max}`;
            }
        }
        
        // Update UI
        if (isValid) {
            field.classList.remove('invalid');
            field.classList.add('valid');
            removeError(field);
        } else {
            field.classList.remove('valid');
            field.classList.add('invalid');
            showError(field, errorMessage);
        }
        
        return isValid;
    }
    
    function showError(field, message) {
        removeError(field);
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.textContent = message;
        
        field.parentNode.appendChild(errorDiv);
    }
    
    function removeError(field) {
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }
    
    function showValidationError() {
        const alert = document.createElement('div');
        alert.className = 'alert alert-error';
        alert.textContent = 'Please fix the errors in the form before submitting.';
        
        predictionForm.insertBefore(alert, predictionForm.firstChild);
        
        setTimeout(() => alert.remove(), 5000);
    }
    
    // ══════════════════════════════════════════════════════════════
    // LOADING STATES
    // ══════════════════════════════════════════════════════════════
    
    function showLoadingState() {
        const submitBtn = predictionForm.querySelector('button[type="submit"]');
        if (submitBtn) {
            const btnText = submitBtn.querySelector('.btn-text');
            const btnLoading = submitBtn.querySelector('.btn-loading');
            
            if (btnText && btnLoading) {
                btnText.style.display = 'none';
                btnLoading.style.display = 'inline';
                submitBtn.disabled = true;
            }
        }
    }
    
    // ══════════════════════════════════════════════════════════════
    // INTERACTIVE SLIDERS
    // ══════════════════════════════════════════════════════════════
    
    const sliders = document.querySelectorAll('input[type="range"]');
    
    sliders.forEach(slider => {
        // Create value display
        const valueDisplay = document.createElement('span');
        valueDisplay.className = 'slider-value';
        valueDisplay.textContent = slider.value;
        
        slider.parentNode.appendChild(valueDisplay);
        
        // Update display on change
        slider.addEventListener('input', function() {
            valueDisplay.textContent = this.value;
        });
    });
    
    // ══════════════════════════════════════════════════════════════
    // CONFIRM DIALOGS
    // ══════════════════════════════════════════════════════════════
    
    const dangerButtons = document.querySelectorAll('[data-confirm]');
    
    dangerButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.dataset.confirm;
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
    
    // ══════════════════════════════════════════════════════════════
    // TOOLTIPS
    // ══════════════════════════════════════════════════════════════
    
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
    
    tooltipTriggers.forEach(trigger => {
        trigger.addEventListener('mouseenter', function(e) {
            showTooltip(this, this.dataset.tooltip);
        });
        
        trigger.addEventListener('mouseleave', function() {
            hideTooltip();
        });
    });
    
    function showTooltip(element, text) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = text;
        
        document.body.appendChild(tooltip);
        
        const rect = element.getBoundingClientRect();
        tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
        tooltip.style.left = (rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
    }
    
    function hideTooltip() {
        const tooltip = document.querySelector('.tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    }
    
    // ══════════════════════════════════════════════════════════════
    // AUTO-HIDE ALERTS
    // ══════════════════════════════════════════════════════════════
    
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
    
    // ══════════════════════════════════════════════════════════════
    // SMOOTH SCROLL
    // ══════════════════════════════════════════════════════════════
    
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId !== '#' && targetId.length > 1) {
                e.preventDefault();
                const target = document.querySelector(targetId);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // ══════════════════════════════════════════════════════════════
    // PRINT FUNCTIONALITY
    // ══════════════════════════════════════════════════════════════
    
    const printButtons = document.querySelectorAll('[data-print]');
    
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            window.print();
        });
    });
    
    // ══════════════════════════════════════════════════════════════
    // COPY TO CLIPBOARD
    // ══════════════════════════════════════════════════════════════
    
    const copyButtons = document.querySelectorAll('[data-copy]');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const text = this.dataset.copy;
            navigator.clipboard.writeText(text).then(() => {
                showNotification('Copied to clipboard!');
            });
        });
    });
    
    function showNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    // ══════════════════════════════════════════════════════════════
    // MOBILE MENU TOGGLE (if needed)
    // ══════════════════════════════════════════════════════════════
    
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // ══════════════════════════════════════════════════════════════
    // FORM AUTO-SAVE (localStorage)
    // ══════════════════════════════════════════════════════════════
    
    if (predictionForm) {
        // Load saved data
        loadFormData();
        
        // Save on input change
        predictionForm.addEventListener('input', debounce(saveFormData, 1000));
        
        // Clear on successful submission
        predictionForm.addEventListener('submit', function() {
            setTimeout(() => localStorage.removeItem('predictionFormData'), 1000);
        });
    }
    
    function saveFormData() {
        const formData = new FormData(predictionForm);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        localStorage.setItem('predictionFormData', JSON.stringify(data));
    }
    
    function loadFormData() {
        const savedData = localStorage.getItem('predictionFormData');
        
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                
                for (let [key, value] of Object.entries(data)) {
                    const field = predictionForm.querySelector(`[name="${key}"]`);
                    if (field) {
                        field.value = value;
                    }
                }
            } catch (e) {
                console.error('Error loading saved form data:', e);
            }
        }
    }
    
    // Utility functions//
    
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // ANALYTICS // 
    
    // Track page views, button clicks, etc.
    // Add your analytics code here if needed
    
    console.log('Student Risk Prediction System initialized');
});

// Custom styles for JS enhanced elements//

const style = document.createElement('style');
style.textContent = `
    /* Form validation styles */
    input.valid, select.valid {
        border-color: var(--success);
    }
    
    input.invalid, select.invalid {
        border-color: var(--danger);
    }
    
    .field-error {
        color: var(--danger);
        font-size: 0.85rem;
        margin-top: 0.25rem;
    }
    
    /* Slider value display */
    .slider-value {
        display: inline-block;
        margin-left: 0.5rem;
        font-weight: 600;
        color: var(--primary);
    }
    
    /* Tooltip */
    .tooltip {
        position: absolute;
        background: var(--gray-900);
        color: white;
        padding: 0.5rem 0.75rem;
        border-radius: 4px;
        font-size: 0.875rem;
        z-index: 1000;
        pointer-events: none;
    }
    
    .tooltip::before {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 50%;
        transform: translateX(-50%);
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid var(--gray-900);
    }
    
    /* Notification */
    .notification {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--success);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.3s;
        z-index: 1000;
    }
    
    .notification.show {
        opacity: 1;
        transform: translateY(0);
    }
    
    /* Alert animations */
    .alert {
        animation: slideDown 0.3s ease-out;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Loading spinner */
    .btn-loading {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Mobile menu (if needed) */
    @media (max-width: 768px) {
        .nav-menu {
            display: none;
        }
        
        .nav-menu.active {
            display: flex;
            flex-direction: column;
        }
    }
`;
document.head.appendChild(style);
