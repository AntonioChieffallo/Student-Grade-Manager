// WebAssembly module loader and configuration
// This file will be replaced by the Emscripten-generated JavaScript when built

// Emscripten module configuration
var Module = {
    onRuntimeInitialized: function() {
        console.log('WebAssembly module runtime initialized');
        // The actual initialization will be handled by app.js
    },
    
    // Customize Emscripten output
    print: function(text) {
        console.log('WASM stdout:', text);
    },
    
    printErr: function(text) {
        console.error('WASM stderr:', text);
    },
    
    // Handle module loading progress
    setStatus: function(text) {
        if (text) {
            console.log('WASM Status:', text);
        }
    },
    
    // Handle errors
    onAbort: function(what) {
        console.error('WASM Aborted:', what);
    },
    
    // Locating the wasm file
    locateFile: function(path, prefix) {
        // In development, the wasm file should be in the same directory
        if (path.endsWith('.wasm')) {
            return 'js/' + path;
        }
        return prefix + path;
    }
};

// Development fallback: If WebAssembly is not available, provide mock functions
if (typeof WebAssembly === 'undefined' || window.location.search.includes('mock=true')) {
    console.warn('WebAssembly not available or mock mode enabled. Using JavaScript fallback.');
    
    // Mock implementation for development/testing
    class MockGradeManager {
        constructor() {
            this.courses = new Map();
        }
        
        addCourse(name, credits) {
            this.courses.set(name, {
                name: name,
                credits: credits,
                grades: []
            });
        }
        
        addGrade(courseName, grade) {
            const course = this.courses.get(courseName);
            if (course && grade >= 0 && grade <= 100) {
                course.grades.push(grade);
            }
        }
        
        getCourseAverage(courseName) {
            const course = this.courses.get(courseName);
            if (!course || course.grades.length === 0) return 0.0;
            
            const sum = course.grades.reduce((a, b) => a + b, 0);
            return sum / course.grades.length;
        }
        
        getGPA() {
            if (this.courses.size === 0) return 0.0;
            
            let totalGradePoints = 0.0;
            let totalCredits = 0;
            
            for (const [name, course] of this.courses) {
                const avg = this.getCourseAverage(name);
                const gradePoints = this.getGradePoints(avg);
                totalGradePoints += gradePoints * course.credits;
                totalCredits += course.credits;
            }
            
            return totalCredits > 0 ? totalGradePoints / totalCredits : 0.0;
        }
        
        getGradePoints(average) {
            if (average >= 97) return 4.0;
            if (average >= 93) return 3.7;
            if (average >= 90) return 3.3;
            if (average >= 87) return 3.0;
            if (average >= 83) return 2.7;
            if (average >= 80) return 2.3;
            if (average >= 77) return 2.0;
            if (average >= 73) return 1.7;
            if (average >= 70) return 1.3;
            if (average >= 67) return 1.0;
            if (average >= 65) return 0.7;
            return 0.0;
        }
        
        getCourseNames() {
            const names = Array.from(this.courses.keys());
            return {
                size: () => names.length,
                get: (index) => names[index]
            };
        }
        
        getCourseCredits(courseName) {
            const course = this.courses.get(courseName);
            return course ? course.credits : 0;
        }
        
        removeCourse(courseName) {
            this.courses.delete(courseName);
        }
        
        clearAll() {
            this.courses.clear();
        }
    }
    
    // Create mock module
    const mockManager = new MockGradeManager();
    
    // Create mock module with functions directly attached
    Module = {
        addCourse: (name, credits) => mockManager.addCourse(name, credits),
        addGrade: (courseName, grade) => mockManager.addGrade(courseName, grade),
        getCourseAverage: (courseName) => mockManager.getCourseAverage(courseName),
        getGPA: () => mockManager.getGPA(),
        getCourseNames: () => mockManager.getCourseNames(),
        getCourseCredits: (courseName) => mockManager.getCourseCredits(courseName),
        removeCourse: (courseName) => mockManager.removeCourse(courseName),
        clearAll: () => mockManager.clearAll(),
        
        onRuntimeInitialized: function() {
            console.log('Mock WebAssembly module initialized');
        }
    };
    
    // Immediately initialize the mock
    setTimeout(() => {
        if (Module.onRuntimeInitialized) {
            Module.onRuntimeInitialized();
        }
    }, 100);
}

// Load the actual WebAssembly module script if available
document.addEventListener('DOMContentLoaded', function() {
    // This will be replaced by the actual Emscripten-generated script when built
    if (typeof WebAssembly !== 'undefined' && !window.location.search.includes('mock=true')) {
        // In a real build, this would load the Emscripten-generated grade_manager.js
        // For now, we use the mock implementation
        console.log('WebAssembly support detected, but using mock implementation for development');
    }
});