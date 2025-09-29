// Global variables
let wasmModule = null;
let isWasmLoaded = false;

// DOM elements
const elements = {
    loading: document.getElementById('loading'),
    errorMessage: document.getElementById('errorMessage'),
    errorText: document.getElementById('errorText'),
    courseName: document.getElementById('courseName'),
    courseCredits: document.getElementById('courseCredits'),
    addCourseBtn: document.getElementById('addCourseBtn'),
    courseSelect: document.getElementById('courseSelect'),
    gradeInput: document.getElementById('gradeInput'),
    addGradeBtn: document.getElementById('addGradeBtn'),
    gpaValue: document.getElementById('gpaValue'),
    calculateGpaBtn: document.getElementById('calculateGpaBtn'),
    coursesList: document.getElementById('coursesList'),
    refreshBtn: document.getElementById('refreshBtn'),
    clearAllBtn: document.getElementById('clearAllBtn')
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

async function initializeApp() {
    try {
        showLoading(true);
        await loadWasmModule();
        setupEventListeners();
        refreshUI();
        showLoading(false);
        console.log('Application initialized successfully');
    } catch (error) {
        console.error('Failed to initialize application:', error);
        showError('Failed to initialize the application. Please refresh the page.');
        showLoading(false);
    }
}

async function loadWasmModule() {
    return new Promise((resolve, reject) => {
        // Check if Module is available (loaded by grade_manager.js)
        if (typeof Module !== 'undefined') {
            Module.onRuntimeInitialized = () => {
                wasmModule = Module;
                isWasmLoaded = true;
                console.log('WebAssembly module loaded successfully');
                resolve();
            };
        } else {
            // Fallback: wait for module to load
            const checkModule = setInterval(() => {
                if (typeof Module !== 'undefined' && Module.onRuntimeInitialized) {
                    clearInterval(checkModule);
                    Module.onRuntimeInitialized = () => {
                        wasmModule = Module;
                        isWasmLoaded = true;
                        console.log('WebAssembly module loaded successfully');
                        resolve();
                    };
                }
            }, 100);
            
            // Timeout after 10 seconds
            setTimeout(() => {
                clearInterval(checkModule);
                reject(new Error('WebAssembly module failed to load within timeout'));
            }, 10000);
        }
    });
}

function setupEventListeners() {
    // Add course
    elements.addCourseBtn.addEventListener('click', addCourse);
    elements.courseName.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addCourse();
    });
    elements.courseCredits.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addCourse();
    });

    // Add grade
    elements.addGradeBtn.addEventListener('click', addGrade);
    elements.gradeInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addGrade();
    });

    // Calculate GPA
    elements.calculateGpaBtn.addEventListener('click', calculateGPA);

    // Action buttons
    elements.refreshBtn.addEventListener('click', refreshUI);
    elements.clearAllBtn.addEventListener('click', clearAllData);
}

function addCourse() {
    try {
        const name = elements.courseName.value.trim();
        const credits = parseInt(elements.courseCredits.value);

        if (!name) {
            showError('Please enter a course name');
            return;
        }

        if (!credits || credits < 1 || credits > 6) {
            showError('Please enter valid credits (1-6)');
            return;
        }

        if (!isWasmLoaded) {
            showError('WebAssembly module not loaded yet');
            return;
        }

        // Call C++ function
        wasmModule.addCourse(name, credits);

        // Clear inputs
        elements.courseName.value = '';
        elements.courseCredits.value = '';

        // Refresh UI
        updateCourseSelect();
        displayCourses();
        calculateGPA();

        console.log(`Added course: ${name} (${credits} credits)`);
    } catch (error) {
        console.error('Error adding course:', error);
        showError('Failed to add course');
    }
}

function addGrade() {
    try {
        const courseName = elements.courseSelect.value;
        const grade = parseFloat(elements.gradeInput.value);

        if (!courseName) {
            showError('Please select a course');
            return;
        }

        if (isNaN(grade) || grade < 0 || grade > 100) {
            showError('Please enter a valid grade (0-100)');
            return;
        }

        if (!isWasmLoaded) {
            showError('WebAssembly module not loaded yet');
            return;
        }

        // Call C++ function
        wasmModule.addGrade(courseName, grade);

        // Clear input
        elements.gradeInput.value = '';

        // Refresh UI
        displayCourses();
        calculateGPA();

        console.log(`Added grade ${grade} to course ${courseName}`);
    } catch (error) {
        console.error('Error adding grade:', error);
        showError('Failed to add grade');
    }
}

function calculateGPA() {
    try {
        if (!isWasmLoaded) {
            elements.gpaValue.textContent = '0.00';
            return;
        }

        const gpa = wasmModule.getGPA();
        elements.gpaValue.textContent = gpa.toFixed(2);
        
        // Add animation effect
        elements.gpaValue.style.transform = 'scale(1.1)';
        setTimeout(() => {
            elements.gpaValue.style.transform = 'scale(1)';
        }, 200);

        console.log(`Calculated GPA: ${gpa.toFixed(2)}`);
    } catch (error) {
        console.error('Error calculating GPA:', error);
        elements.gpaValue.textContent = '0.00';
        showError('Failed to calculate GPA');
    }
}

function updateCourseSelect() {
    try {
        if (!isWasmLoaded) return;

        const courseNames = wasmModule.getCourseNames();
        const select = elements.courseSelect;
        
        // Clear existing options except the first one
        select.innerHTML = '<option value="">Select a course</option>';
        
        // Add course options
        for (let i = 0; i < courseNames.size(); i++) {
            const name = courseNames.get(i);
            const option = document.createElement('option');
            option.value = name;
            option.textContent = name;
            select.appendChild(option);
        }
    } catch (error) {
        console.error('Error updating course select:', error);
    }
}

function displayCourses() {
    try {
        if (!isWasmLoaded) {
            elements.coursesList.innerHTML = '<p class="no-courses">WebAssembly module loading...</p>';
            return;
        }

        const courseNames = wasmModule.getCourseNames();
        
        if (courseNames.size() === 0) {
            elements.coursesList.innerHTML = '<p class="no-courses">No courses added yet. Add your first course above!</p>';
            return;
        }

        let html = '';
        for (let i = 0; i < courseNames.size(); i++) {
            const name = courseNames.get(i);
            const credits = wasmModule.getCourseCredits(name);
            const average = wasmModule.getCourseAverage(name);
            
            html += createCourseCard(name, credits, average);
        }
        
        elements.coursesList.innerHTML = html;
        
        // Add event listeners for remove buttons
        document.querySelectorAll('.remove-course').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const courseName = e.target.dataset.course;
                removeCourse(courseName);
            });
        });
    } catch (error) {
        console.error('Error displaying courses:', error);
        elements.coursesList.innerHTML = '<p class="no-courses">Error loading courses</p>';
    }
}

function createCourseCard(name, credits, average) {
    let gradeColor = '#7f8c8d'; // Default gray
    if (average >= 90) gradeColor = '#27ae60'; // Green
    else if (average >= 80) gradeColor = '#f39c12'; // Orange
    else if (average >= 70) gradeColor = '#e67e22'; // Dark orange
    else if (average > 0) gradeColor = '#e74c3c'; // Red
    
    return `
        <div class="course-card">
            <div class="course-header">
                <div class="course-name">${name}</div>
                <div class="course-credits">${credits} Credits</div>
            </div>
            <div class="course-stats">
                <div class="stat">
                    <div class="stat-value" style="color: ${gradeColor}">
                        ${average > 0 ? average.toFixed(1) : 'N/A'}
                    </div>
                    <div class="stat-label">Average</div>
                </div>
                <div class="stat">
                    <div class="stat-value" style="color: ${gradeColor}">
                        ${average > 0 ? getLetterGrade(average) : 'N/A'}
                    </div>
                    <div class="stat-label">Letter Grade</div>
                </div>
            </div>
            <div class="course-actions">
                <button class="btn btn-small btn-danger remove-course" data-course="${name}">
                    Remove Course
                </button>
            </div>
        </div>
    `;
}

function getLetterGrade(average) {
    if (average >= 97) return 'A+';
    if (average >= 93) return 'A';
    if (average >= 90) return 'A-';
    if (average >= 87) return 'B+';
    if (average >= 83) return 'B';
    if (average >= 80) return 'B-';
    if (average >= 77) return 'C+';
    if (average >= 73) return 'C';
    if (average >= 70) return 'C-';
    if (average >= 67) return 'D+';
    if (average >= 65) return 'D';
    return 'F';
}

function removeCourse(courseName) {
    try {
        if (!isWasmLoaded) {
            showError('WebAssembly module not loaded yet');
            return;
        }

        if (confirm(`Are you sure you want to remove "${courseName}"?`)) {
            wasmModule.removeCourse(courseName);
            updateCourseSelect();
            displayCourses();
            calculateGPA();
            console.log(`Removed course: ${courseName}`);
        }
    } catch (error) {
        console.error('Error removing course:', error);
        showError('Failed to remove course');
    }
}

function clearAllData() {
    try {
        if (!isWasmLoaded) {
            showError('WebAssembly module not loaded yet');
            return;
        }

        if (confirm('Are you sure you want to clear all courses and grades? This action cannot be undone.')) {
            wasmModule.clearAll();
            refreshUI();
            console.log('Cleared all data');
        }
    } catch (error) {
        console.error('Error clearing data:', error);
        showError('Failed to clear data');
    }
}

function refreshUI() {
    updateCourseSelect();
    displayCourses();
    calculateGPA();
}

function showLoading(show) {
    elements.loading.style.display = show ? 'flex' : 'none';
}

function showError(message) {
    elements.errorText.textContent = message;
    elements.errorMessage.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    elements.errorMessage.style.display = 'none';
}

// Make hideError available globally for the HTML onclick
window.hideError = hideError;