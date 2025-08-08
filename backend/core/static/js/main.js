// Main JavaScript for Screenwise Platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeDropdown();
    initializeProgress();
    initializeVideoPlayer();
    initializeAnalytics();
});

// Mobile menu functionality
function initializeDropdown() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

// Progress bar animations
function initializeProgress() {
    const progressBars = document.querySelectorAll('.progress-fill');
    
    progressBars.forEach(bar => {
        const targetWidth = bar.dataset.progress;
        if (targetWidth) {
            setTimeout(() => {
                bar.style.width = targetWidth + '%';
            }, 500);
        }
    });
}

// Video player enhancements
function initializeVideoPlayer() {
    const videoElements = document.querySelectorAll('video');
    
    videoElements.forEach(video => {
        video.addEventListener('loadedmetadata', function() {
            // Update duration display if needed
            const duration = this.duration;
            const durationDisplay = this.parentElement.querySelector('.duration-display');
            if (durationDisplay) {
                durationDisplay.textContent = formatDuration(duration);
            }
        });

        video.addEventListener('timeupdate', function() {
            // Track watch progress for analytics
            const progress = (this.currentTime / this.duration) * 100;
            updateWatchProgress(this.dataset.videoId, progress);
        });
    });
}

// Analytics tracking
function initializeAnalytics() {
    // Track time spent on page
    const startTime = Date.now();
    
    window.addEventListener('beforeunload', function() {
        const timeSpent = Date.now() - startTime;
        trackTimeSpent(timeSpent);
    });
    
    // Track scroll behavior
    let scrollTimeout;
    window.addEventListener('scroll', function() {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            trackScrollBehavior();
        }, 1000);
    });
}

// Utility functions
function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
}

function updateWatchProgress(videoId, progress) {
    // Send AJAX request to update watch progress
    if (progress > 80) { // Consider video completed at 80%
        fetch('/api/video/complete/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                video_id: videoId,
                progress: progress
            })
        });
    }
}

function trackTimeSpent(timeSpent) {
    // Track how much time user spent on the page
    fetch('/api/analytics/time/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            time_spent: timeSpent,
            page: window.location.pathname
        })
    });
}

function trackScrollBehavior() {
    // Detect if user is doom scrolling
    const scrollPosition = window.scrollY;
    const documentHeight = document.documentElement.scrollHeight;
    const viewportHeight = window.innerHeight;
    
    const scrollPercentage = (scrollPosition / (documentHeight - viewportHeight)) * 100;
    
    if (scrollPercentage > 90) {
        // User scrolled to bottom, might be doom scrolling
        fetch('/api/analytics/scroll/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                scroll_percentage: scrollPercentage,
                page: window.location.pathname
            })
        });
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Form enhancements
function initializeForms() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Loading...';
            }
        });
    });
}

// Video upload drag and drop
function initializeFileUpload() {
    const dropZones = document.querySelectorAll('.drop-zone');
    
    dropZones.forEach(dropZone => {
        const fileInput = dropZone.querySelector('input[type="file"]');
        
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });
        
        dropZone.addEventListener('drop', handleDrop, false);
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        function highlight(e) {
            dropZone.classList.add('border-gray-800', 'bg-gray-50');
        }
        
        function unhighlight(e) {
            dropZone.classList.remove('border-gray-800', 'bg-gray-50');
        }
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                fileInput.files = files;
                updateFileDisplay(files[0].name);
            }
        }
    });
}

function updateFileDisplay(fileName) {
    const fileNameDisplay = document.querySelector('.file-name-display');
    if (fileNameDisplay) {
        fileNameDisplay.textContent = `Selected: ${fileName}`;
    }
}
