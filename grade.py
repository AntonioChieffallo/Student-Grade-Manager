"""
Core classes for the Student Grade Manager system.
"""

from typing import List, Dict, Optional
from enum import Enum


class GradeType(Enum):
    """Enumeration for different types of grades."""
    HOMEWORK = "homework"
    EXAM = "exam"
    QUIZ = "quiz"


class Grade:
    """Represents a single grade for an assignment."""
    
    def __init__(self, name: str, score: float, total_points: float, grade_type: GradeType):
        """
        Initialize a Grade object.
        
        Args:
            name: Name of the assignment
            score: Points earned
            total_points: Total points possible
            grade_type: Type of grade (homework, exam, quiz)
        """
        if score < 0 or total_points <= 0:
            raise ValueError("Score must be non-negative and total points must be positive")
        if score > total_points:
            raise ValueError("Score cannot exceed total points")
            
        self.name = name
        self.score = score
        self.total_points = total_points
        self.grade_type = grade_type
    
    @property
    def percentage(self) -> float:
        """Calculate the percentage score."""
        return (self.score / self.total_points) * 100
    
    def __str__(self) -> str:
        return f"{self.name}: {self.score}/{self.total_points} ({self.percentage:.2f}%)"


class GradeCategory:
    """Represents a category of grades (homework, exams, quizzes)."""
    
    def __init__(self, grade_type: GradeType):
        """
        Initialize a GradeCategory.
        
        Args:
            grade_type: The type of grades this category contains
        """
        self.grade_type = grade_type
        self.grades: List[Grade] = []
    
    def add_grade(self, grade: Grade) -> None:
        """Add a grade to this category."""
        if grade.grade_type != self.grade_type:
            raise ValueError(f"Grade type {grade.grade_type} doesn't match category type {self.grade_type}")
        self.grades.append(grade)
    
    def total_points_earned(self) -> float:
        """Calculate total points earned in this category."""
        return sum(grade.score for grade in self.grades)
    
    def total_points_possible(self) -> float:
        """Calculate total points possible in this category."""
        return sum(grade.total_points for grade in self.grades)
    
    def category_percentage(self) -> float:
        """Calculate the percentage for this category."""
        total_possible = self.total_points_possible()
        if total_possible == 0:
            return 0.0
        return (self.total_points_earned() / total_possible) * 100
    
    def __len__(self) -> int:
        return len(self.grades)
    
    def __str__(self) -> str:
        if not self.grades:
            return f"{self.grade_type.value.title()}: No grades"
        return f"{self.grade_type.value.title()}: {self.total_points_earned()}/{self.total_points_possible()} ({self.category_percentage():.2f}%)"


class Course:
    """Represents a single course with multiple grade categories."""
    
    def __init__(self, name: str, credit_hours: float = 3.0):
        """
        Initialize a Course.
        
        Args:
            name: Name of the course
            credit_hours: Number of credit hours for the course
        """
        self.name = name
        self.credit_hours = credit_hours
        self.categories: Dict[GradeType, GradeCategory] = {
            GradeType.HOMEWORK: GradeCategory(GradeType.HOMEWORK),
            GradeType.EXAM: GradeCategory(GradeType.EXAM),
            GradeType.QUIZ: GradeCategory(GradeType.QUIZ)
        }
    
    def add_grade(self, grade: Grade) -> None:
        """Add a grade to the appropriate category."""
        self.categories[grade.grade_type].add_grade(grade)
    
    def total_points_earned(self) -> float:
        """Calculate total points earned across all categories."""
        return sum(category.total_points_earned() for category in self.categories.values())
    
    def total_points_possible(self) -> float:
        """Calculate total points possible across all categories."""
        return sum(category.total_points_possible() for category in self.categories.values())
    
    def course_percentage(self) -> float:
        """Calculate the overall course percentage."""
        total_possible = self.total_points_possible()
        if total_possible == 0:
            return 0.0
        return (self.total_points_earned() / total_possible) * 100
    
    def letter_grade(self) -> str:
        """Convert percentage to letter grade."""
        percentage = self.course_percentage()
        if percentage >= 97:
            return "A+"
        elif percentage >= 93:
            return "A"
        elif percentage >= 90:
            return "A-"
        elif percentage >= 87:
            return "B+"
        elif percentage >= 83:
            return "B"
        elif percentage >= 80:
            return "B-"
        elif percentage >= 77:
            return "C+"
        elif percentage >= 73:
            return "C"
        elif percentage >= 70:
            return "C-"
        elif percentage >= 67:
            return "D+"
        elif percentage >= 63:
            return "D"
        elif percentage >= 60:
            return "D-"
        else:
            return "F"
    
    def grade_points(self) -> float:
        """Convert letter grade to grade points for GPA calculation."""
        letter = self.letter_grade()
        grade_map = {
            "A+": 4.0, "A": 4.0, "A-": 3.7,
            "B+": 3.3, "B": 3.0, "B-": 2.7,
            "C+": 2.3, "C": 2.0, "C-": 1.7,
            "D+": 1.3, "D": 1.0, "D-": 0.7,
            "F": 0.0
        }
        return grade_map.get(letter, 0.0)
    
    def what_if_grade(self, hypothetical_grade: Grade) -> float:
        """
        Calculate what the course percentage would be if a hypothetical grade were added.
        
        Args:
            hypothetical_grade: The grade to simulate adding
            
        Returns:
            The new course percentage if this grade were added
        """
        current_earned = self.total_points_earned()
        current_possible = self.total_points_possible()
        
        new_earned = current_earned + hypothetical_grade.score
        new_possible = current_possible + hypothetical_grade.total_points
        
        if new_possible == 0:
            return 0.0
        return (new_earned / new_possible) * 100
    
    def __str__(self) -> str:
        result = [f"Course: {self.name} ({self.credit_hours} credit hours)"]
        result.append(f"Overall: {self.total_points_earned()}/{self.total_points_possible()} ({self.course_percentage():.2f}%) - {self.letter_grade()}")
        result.append("")
        for category in self.categories.values():
            if len(category) > 0:
                result.append(str(category))
                for grade in category.grades:
                    result.append(f"  - {grade}")
                result.append("")
        return "\n".join(result)


class Student:
    """Represents a student with multiple courses."""
    
    def __init__(self, name: str):
        """
        Initialize a Student.
        
        Args:
            name: Name of the student
        """
        self.name = name
        self.courses: Dict[str, Course] = {}
    
    def add_course(self, course: Course) -> None:
        """Add a course to the student's course list."""
        self.courses[course.name] = course
    
    def remove_course(self, course_name: str) -> None:
        """Remove a course from the student's course list."""
        if course_name in self.courses:
            del self.courses[course_name]
    
    def calculate_gpa(self) -> float:
        """Calculate the student's GPA across all courses."""
        if not self.courses:
            return 0.0
        
        total_grade_points = 0.0
        total_credit_hours = 0.0
        
        for course in self.courses.values():
            # Only include courses that have grades
            if course.total_points_possible() > 0:
                total_grade_points += course.grade_points() * course.credit_hours
                total_credit_hours += course.credit_hours
        
        if total_credit_hours == 0:
            return 0.0
        
        return total_grade_points / total_credit_hours
    
    def what_if_course_grade(self, course_name: str, hypothetical_grade: Grade) -> Optional[float]:
        """
        Calculate what the student's GPA would be if a hypothetical grade were added to a course.
        
        Args:
            course_name: Name of the course to add the grade to
            hypothetical_grade: The grade to simulate adding
            
        Returns:
            The new GPA if this grade were added, or None if the course doesn't exist
        """
        if course_name not in self.courses:
            return None
        
        # Temporarily add the grade to calculate new GPA
        course = self.courses[course_name]
        original_grades = course.categories[hypothetical_grade.grade_type].grades.copy()
        
        course.add_grade(hypothetical_grade)
        new_gpa = self.calculate_gpa()
        
        # Restore original grades
        course.categories[hypothetical_grade.grade_type].grades = original_grades
        
        return new_gpa
    
    def __str__(self) -> str:
        result = [f"Student: {self.name}"]
        result.append(f"GPA: {self.calculate_gpa():.2f}")
        result.append("")
        
        for course in self.courses.values():
            result.append(str(course))
            result.append("-" * 50)
        
        return "\n".join(result)