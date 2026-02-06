// Main JavaScript file for NEET/JEE Learning App

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});

// Test-related functions
function saveTestProgress() {
    if (typeof(Storage) !== "undefined") {
        var answers = {};
        var radioButtons = document.querySelectorAll('input[type="radio"]:checked');
        
        radioButtons.forEach(function(radio) {
            answers[radio.name] = radio.value;
        });
        
        localStorage.setItem('testProgress', JSON.stringify({
            answers: answers,
            timestamp: new Date().toISOString()
        }));
    }
}

function loadTestProgress() {
    if (typeof(Storage) !== "undefined") {
        var saved = localStorage.getItem('testProgress');
        if (saved) {
            var progress = JSON.parse(saved);
            
            // Check if saved progress is from today
            var savedDate = new Date(progress.timestamp);
            var today = new Date();
            
            if (savedDate.toDateString() === today.toDateString()) {
                for (var questionName in progress.answers) {
                    var radio = document.querySelector(`input[name="${questionName}"][value="${progress.answers[questionName]}"]`);
                    if (radio) {
                        radio.checked = true;
                    }
                }
                
                // Update question navigator
                if (typeof updateQuestionStatus === 'function') {
                    updateQuestionStatus();
                }
            }
        }
    }
}

// Auto-save test progress every 30 seconds
setInterval(function() {
    if (document.querySelector('input[type="radio"]')) {
        saveTestProgress();
    }
}, 30000);

// Load saved progress when test page loads
if (document.querySelector('input[type="radio"]')) {
    loadTestProgress();
}

// Confirmation dialogs
function confirmAction(message) {
    return confirm(message || 'Are you sure you want to proceed?');
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        var target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Performance chart helper (if Chart.js is loaded)
function createPerformanceChart(canvasId, labels, data) {
    if (typeof Chart !== 'undefined') {
        var ctx = document.getElementById(canvasId);
        if (ctx) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Performance (%)',
                        data: data,
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        tension: 0.1,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: {
                                callback: function(value) {
                                    return value + '%';
                                }
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
        }
    }
}

// Utility functions
function formatTime(seconds) {
    var minutes = Math.floor(seconds / 60);
    var remainingSeconds = seconds % 60;
    return minutes.toString().padStart(2, '0') + ':' + remainingSeconds.toString().padStart(2, '0');
}

function showLoading(element) {
    if (element) {
        element.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
        element.disabled = true;
    }
}

function hideLoading(element, originalText) {
    if (element) {
        element.innerHTML = originalText || 'Submit';
        element.disabled = false;
    }
}

// Subject color mapping
const subjectColors = {
    'Physics': '#007bff',
    'Chemistry': '#28a745',
    'Biology': '#dc3545',
    'Mathematics': '#ffc107'
};

function getSubjectColor(subject) {
    return subjectColors[subject] || '#6c757d';
}

// Local storage helpers
function saveToLocalStorage(key, data) {
    if (typeof(Storage) !== "undefined") {
        localStorage.setItem(key, JSON.stringify(data));
    }
}

function getFromLocalStorage(key) {
    if (typeof(Storage) !== "undefined") {
        var data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    }
    return null;
}

// Clear test progress when test is submitted
document.addEventListener('submit', function(e) {
    if (e.target.id === 'testForm') {
        localStorage.removeItem('testProgress');
    }
});