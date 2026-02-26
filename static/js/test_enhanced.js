// Test Security and Functionality
let testTimer;
let timeRemaining;
let tabSwitchCount = 0;
let testSubmitted = false;

function initializeTest(duration, form, submitUrl) {
    timeRemaining = duration;
    
    // Start timer
    startTimer();
    
    // Setup event listeners
    setupEventListeners(form, submitUrl);
    
    // Monitor fullscreen
    monitorFullscreen(form, submitUrl);
    
    // Monitor tab visibility
    monitorTabVisibility(form, submitUrl);
    
    // Monitor AI tools (basic detection)
    monitorAITools(form, submitUrl);
    
    // Update question status
    updateQuestionStatus();
    
    // Prevent context menu
    document.addEventListener('contextmenu', e => e.preventDefault());
    
    // Prevent certain keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Prevent F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U
        if (e.keyCode === 123 || 
            (e.ctrlKey && e.shiftKey && (e.keyCode === 73 || e.keyCode === 74)) ||
            (e.ctrlKey && e.keyCode === 85)) {
            e.preventDefault();
            return false;
        }
    });
}

function startTimer() {
    updateTimerDisplay();
    
    testTimer = setInterval(() => {
        timeRemaining--;
        updateTimerDisplay();
        
        // Warning at 5 minutes
        if (timeRemaining === 300) {
            showNotification('warning', '5 minutes remaining!');
            document.getElementById('timer').classList.add('warning');
        }
        
        // Auto-submit when time expires
        if (timeRemaining <= 0) {
            clearInterval(testTimer);
            showNotification('error', 'Time expired! Submitting test...');
            setTimeout(() => autoSubmitTest(), 2000);
        }
    }, 1000);
}

function updateTimerDisplay() {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    const display = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    document.getElementById('timerDisplay').textContent = display;
}

function setupEventListeners(form, submitUrl) {
    // Radio button changes
    document.querySelectorAll('.option-input').forEach(input => {
        input.addEventListener('change', function() {
            updateQuestionStatus();
            markQuestionAsAnswered(this.closest('.question-card'));
        });
    });
    
    // Clear response buttons
    document.querySelectorAll('.clear-response').forEach(btn => {
        btn.addEventListener('click', function() {
            const questionId = this.dataset.question;
            document.querySelectorAll(`input[name="question_${questionId}"]`).forEach(input => {
                input.checked = false;
            });
            updateQuestionStatus();
        });
    });
    
    // Mark for review buttons
    document.querySelectorAll('.mark-review').forEach(btn => {
        btn.addEventListener('click', function() {
            const questionNum = this.dataset.question;
            const card = document.getElementById(`question-${questionNum}`);
            const navBtn = document.querySelector(`.nav-btn[data-question="${questionNum}"]`);
            
            card.classList.toggle('marked');
            navBtn.classList.toggle('marked');
        });
    });
    
    // Submit button
    document.getElementById('submitTestBtn').addEventListener('click', function() {
        if (confirm('Are you sure you want to submit the test? You cannot change your answers after submission.')) {
            submitTest(form);
        }
    });
}

function monitorFullscreen(form, submitUrl) {
    document.addEventListener('fullscreenchange', function() {
        if (!document.fullscreenElement && !testSubmitted) {
            handleMalpractice('Exited fullscreen mode', form);
        }
    });
    
    document.addEventListener('webkitfullscreenchange', function() {
        if (!document.webkitFullscreenElement && !testSubmitted) {
            handleMalpractice('Exited fullscreen mode', form);
        }
    });
}

function monitorTabVisibility(form, submitUrl) {
    document.addEventListener('visibilitychange', function() {
        if (document.hidden && !testSubmitted) {
            tabSwitchCount++;
            
            if (tabSwitchCount >= 1) {
                handleMalpractice('Switched tabs/windows', form);
            } else {
                showNotification('warning', 'Warning: Do not switch tabs! Next violation will submit your test.');
            }
        }
    });
    
    window.addEventListener('blur', function() {
        if (!testSubmitted && document.hasFocus() === false) {
            // Window lost focus
            console.log('Window lost focus');
        }
    });
}

function monitorAITools(form, submitUrl) {
    // Detect if DevTools is open (basic detection)
    const devtools = /./;
    devtools.toString = function() {
        handleMalpractice('Developer tools detected', form);
    };
    
    // Monitor clipboard
    document.addEventListener('copy', function(e) {
        if (!testSubmitted) {
            showNotification('warning', 'Copying content is not allowed during the test');
            e.preventDefault();
        }
    });
    
    document.addEventListener('paste', function(e) {
        if (!testSubmitted) {
            showNotification('warning', 'Pasting content is not allowed during the test');
            e.preventDefault();
        }
    });
}

function handleMalpractice(reason, form) {
    if (testSubmitted) return;
    
    console.log('Malpractice detected:', reason);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('malpracticeModal'));
    modal.show();
    
    // Submit test after 3 seconds
    setTimeout(() => {
        autoSubmitTest();
    }, 3000);
}

function autoSubmitTest() {
    if (testSubmitted) return;
    
    testSubmitted = true;
    clearInterval(testTimer);
    
    const form = document.getElementById('testForm');
    form.submit();
}

function submitTest(form) {
    if (testSubmitted) return;
    
    testSubmitted = true;
    clearInterval(testTimer);
    form.submit();
}

function updateQuestionStatus() {
    const totalQuestions = document.querySelectorAll('.question-card').length;
    let answeredCount = 0;
    
    document.querySelectorAll('.question-card').forEach((card, index) => {
        const questionId = card.dataset.questionId;
        const isAnswered = document.querySelector(`input[name="question_${questionId}"]:checked`);
        const navBtn = document.querySelector(`.nav-btn[data-question="${index + 1}"]`);
        
        if (isAnswered) {
            answeredCount++;
            navBtn.classList.add('answered');
        } else {
            navBtn.classList.remove('answered');
        }
    });
    
    document.querySelector('.answered-count').textContent = answeredCount;
}

function markQuestionAsAnswered(card) {
    card.classList.add('answered');
}

function scrollToQuestion(questionNum) {
    const card = document.getElementById(`question-${questionNum}`);
    const offset = 100;
    const elementPosition = card.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - offset;
    
    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
    
    // Highlight current question
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('current'));
    document.querySelector(`.nav-btn[data-question="${questionNum}"]`).classList.add('current');
}

function showNotification(type, message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'warning' ? 'warning' : 'danger'} alert-dismissible fade show`;
    notification.style.cssText = 'position: fixed; top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        <i class="fas fa-${type === 'warning' ? 'exclamation-triangle' : 'ban'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Prevent page unload without confirmation
window.addEventListener('beforeunload', function(e) {
    if (!testSubmitted) {
        e.preventDefault();
        e.returnValue = '';
        return '';
    }
});

// Auto-save progress every 30 seconds
setInterval(() => {
    if (!testSubmitted && typeof(Storage) !== "undefined") {
        const answers = {};
        document.querySelectorAll('.option-input:checked').forEach(input => {
            answers[input.name] = input.value;
        });
        
        localStorage.setItem('testProgress', JSON.stringify({
            answers: answers,
            timeRemaining: timeRemaining,
            timestamp: new Date().toISOString()
        }));
    }
}, 30000);

// Load saved progress on page load
window.addEventListener('load', function() {
    if (typeof(Storage) !== "undefined") {
        const saved = localStorage.getItem('testProgress');
        if (saved) {
            const progress = JSON.parse(saved);
            const savedDate = new Date(progress.timestamp);
            const now = new Date();
            
            // Only restore if saved within last hour
            if ((now - savedDate) < 3600000) {
                for (let questionName in progress.answers) {
                    const input = document.querySelector(`input[name="${questionName}"][value="${progress.answers[questionName]}"]`);
                    if (input) {
                        input.checked = true;
                    }
                }
                updateQuestionStatus();
            }
        }
    }
});
