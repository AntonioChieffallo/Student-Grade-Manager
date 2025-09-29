#include <emscripten/bind.h>
#include <vector>
#include <string>
#include <map>
#include <numeric>

class Course {
public:
    std::string name;
    std::vector<double> grades;
    int credits;
    
    Course(const std::string& courseName, int courseCredits) 
        : name(courseName), credits(courseCredits) {}
    
    void addGrade(double grade) {
        if (grade >= 0.0 && grade <= 100.0) {
            grades.push_back(grade);
        }
    }
    
    double getAverage() const {
        if (grades.empty()) return 0.0;
        double sum = std::accumulate(grades.begin(), grades.end(), 0.0);
        return sum / grades.size();
    }
    
    double getGradePoints() const {
        double avg = getAverage();
        if (avg >= 97) return 4.0;
        if (avg >= 93) return 3.7;
        if (avg >= 90) return 3.3;
        if (avg >= 87) return 3.0;
        if (avg >= 83) return 2.7;
        if (avg >= 80) return 2.3;
        if (avg >= 77) return 2.0;
        if (avg >= 73) return 1.7;
        if (avg >= 70) return 1.3;
        if (avg >= 67) return 1.0;
        if (avg >= 65) return 0.7;
        return 0.0;
    }
};

class GradeManager {
private:
    std::map<std::string, Course> courses;
    
public:
    void addCourse(const std::string& name, int credits) {
        courses.emplace(name, Course(name, credits));
    }
    
    void addGrade(const std::string& courseName, double grade) {
        auto it = courses.find(courseName);
        if (it != courses.end()) {
            it->second.addGrade(grade);
        }
    }
    
    double getCourseAverage(const std::string& courseName) const {
        auto it = courses.find(courseName);
        if (it != courses.end()) {
            return it->second.getAverage();
        }
        return 0.0;
    }
    
    double getGPA() const {
        if (courses.empty()) return 0.0;
        
        double totalGradePoints = 0.0;
        int totalCredits = 0;
        
        for (const auto& pair : courses) {
            const Course& course = pair.second;
            totalGradePoints += course.getGradePoints() * course.credits;
            totalCredits += course.credits;
        }
        
        return totalCredits > 0 ? totalGradePoints / totalCredits : 0.0;
    }
    
    std::vector<std::string> getCourseNames() const {
        std::vector<std::string> names;
        for (const auto& pair : courses) {
            names.push_back(pair.first);
        }
        return names;
    }
    
    int getCourseCredits(const std::string& courseName) const {
        auto it = courses.find(courseName);
        if (it != courses.end()) {
            return it->second.credits;
        }
        return 0;
    }
    
    void removeCourse(const std::string& courseName) {
        courses.erase(courseName);
    }
    
    void clearAll() {
        courses.clear();
    }
};

// Global instance
GradeManager gradeManager;

// Exported functions for JavaScript
EMSCRIPTEN_BINDINGS(grade_manager) {
    emscripten::class_<GradeManager>("GradeManager")
        .constructor<>()
        .function("addCourse", &GradeManager::addCourse)
        .function("addGrade", &GradeManager::addGrade)
        .function("getCourseAverage", &GradeManager::getCourseAverage)
        .function("getGPA", &GradeManager::getGPA)
        .function("getCourseNames", &GradeManager::getCourseNames)
        .function("getCourseCredits", &GradeManager::getCourseCredits)
        .function("removeCourse", &GradeManager::removeCourse)
        .function("clearAll", &GradeManager::clearAll);
    
    // Export global instance
    emscripten::function("getGradeManager", []() -> GradeManager& {
        return gradeManager;
    }, emscripten::allow_raw_pointers());
    
    // Convenience functions for direct access
    emscripten::function("addCourse", [](const std::string& name, int credits) {
        gradeManager.addCourse(name, credits);
    });
    
    emscripten::function("addGrade", [](const std::string& courseName, double grade) {
        gradeManager.addGrade(courseName, grade);
    });
    
    emscripten::function("getCourseAverage", [](const std::string& courseName) -> double {
        return gradeManager.getCourseAverage(courseName);
    });
    
    emscripten::function("getGPA", []() -> double {
        return gradeManager.getGPA();
    });
    
    emscripten::function("getCourseNames", []() -> std::vector<std::string> {
        return gradeManager.getCourseNames();
    });
    
    emscripten::function("getCourseCredits", [](const std::string& courseName) -> int {
        return gradeManager.getCourseCredits(courseName);
    });
    
    emscripten::function("removeCourse", [](const std::string& courseName) {
        gradeManager.removeCourse(courseName);
    });
    
    emscripten::function("clearAll", []() {
        gradeManager.clearAll();
    });
    
    // Register vector types
    emscripten::register_vector<std::string>("VectorString");
}