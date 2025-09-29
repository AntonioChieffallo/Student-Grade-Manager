#!/usr/bin/env python3
"""
Unit tests for the Student Grade Manager system.
"""

import unittest
from grade import Grade, GradeType, GradeCategory, Course, Student


class TestGrade(unittest.TestCase):
    """Test cases for the Grade class."""
    
    def test_grade_creation(self):
        """Test basic grade creation."""
        grade = Grade("HW1", 85, 100, GradeType.HOMEWORK)
        self.assertEqual(grade.name, "HW1")
        self.assertEqual(grade.score, 85)
        self.assertEqual(grade.total_points, 100)
        self.assertEqual(grade.grade_type, GradeType.HOMEWORK)
        self.assertEqual(grade.percentage, 85.0)
    
    def test_grade_percentage_calculation(self):
        """Test percentage calculation."""
        grade = Grade("Quiz1", 18, 20, GradeType.QUIZ)
        self.assertEqual(grade.percentage, 90.0)
    
    def test_invalid_grade_values(self):
        """Test that invalid grade values raise exceptions."""
        with self.assertRaises(ValueError):
            Grade("Invalid", -5, 100, GradeType.HOMEWORK)  # Negative score
        
        with self.assertRaises(ValueError):
            Grade("Invalid", 50, 0, GradeType.HOMEWORK)  # Zero total points
        
        with self.assertRaises(ValueError):
            Grade("Invalid", 110, 100, GradeType.HOMEWORK)  # Score > total


class TestGradeCategory(unittest.TestCase):
    """Test cases for the GradeCategory class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.hw_category = GradeCategory(GradeType.HOMEWORK)
        self.hw1 = Grade("HW1", 85, 100, GradeType.HOMEWORK)
        self.hw2 = Grade("HW2", 90, 100, GradeType.HOMEWORK)
    
    def test_add_grade(self):
        """Test adding grades to a category."""
        self.hw_category.add_grade(self.hw1)
        self.assertEqual(len(self.hw_category), 1)
        
        self.hw_category.add_grade(self.hw2)
        self.assertEqual(len(self.hw_category), 2)
    
    def test_wrong_grade_type(self):
        """Test that adding wrong grade type raises exception."""
        exam_grade = Grade("Exam1", 80, 100, GradeType.EXAM)
        with self.assertRaises(ValueError):
            self.hw_category.add_grade(exam_grade)
    
    def test_category_calculations(self):
        """Test category total and percentage calculations."""
        self.hw_category.add_grade(self.hw1)
        self.hw_category.add_grade(self.hw2)
        
        self.assertEqual(self.hw_category.total_points_earned(), 175)
        self.assertEqual(self.hw_category.total_points_possible(), 200)
        self.assertEqual(self.hw_category.category_percentage(), 87.5)
    
    def test_empty_category(self):
        """Test empty category calculations."""
        self.assertEqual(self.hw_category.total_points_earned(), 0)
        self.assertEqual(self.hw_category.total_points_possible(), 0)
        self.assertEqual(self.hw_category.category_percentage(), 0.0)


class TestCourse(unittest.TestCase):
    """Test cases for the Course class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.course = Course("CS101", 3.0)
        self.hw1 = Grade("HW1", 85, 100, GradeType.HOMEWORK)
        self.hw2 = Grade("HW2", 90, 100, GradeType.HOMEWORK)
        self.exam1 = Grade("Midterm", 78, 100, GradeType.EXAM)
        self.quiz1 = Grade("Quiz1", 18, 20, GradeType.QUIZ)
    
    def test_course_creation(self):
        """Test basic course creation."""
        self.assertEqual(self.course.name, "CS101")
        self.assertEqual(self.course.credit_hours, 3.0)
        self.assertEqual(len(self.course.categories), 3)
    
    def test_add_grades(self):
        """Test adding grades to course."""
        self.course.add_grade(self.hw1)
        self.course.add_grade(self.hw2)
        self.course.add_grade(self.exam1)
        self.course.add_grade(self.quiz1)
        
        self.assertEqual(len(self.course.categories[GradeType.HOMEWORK]), 2)
        self.assertEqual(len(self.course.categories[GradeType.EXAM]), 1)
        self.assertEqual(len(self.course.categories[GradeType.QUIZ]), 1)
    
    def test_course_calculations(self):
        """Test course total and percentage calculations."""
        self.course.add_grade(self.hw1)
        self.course.add_grade(self.hw2)
        self.course.add_grade(self.exam1)
        self.course.add_grade(self.quiz1)
        
        # Total: 85 + 90 + 78 + 18 = 271 out of 320
        self.assertEqual(self.course.total_points_earned(), 271)
        self.assertEqual(self.course.total_points_possible(), 320)
        self.assertAlmostEqual(self.course.course_percentage(), 84.6875, places=4)
    
    def test_letter_grades(self):
        """Test letter grade conversion."""
        # Test A grade (97+)
        grade_a = Grade("Perfect", 97, 100, GradeType.EXAM)
        course_a = Course("Test", 3.0)
        course_a.add_grade(grade_a)
        self.assertEqual(course_a.letter_grade(), "A+")
        
        # Test B grade (83-86.99)
        grade_b = Grade("Good", 85, 100, GradeType.EXAM)
        course_b = Course("Test", 3.0)
        course_b.add_grade(grade_b)
        self.assertEqual(course_b.letter_grade(), "B")
        
        # Test F grade (<60)
        grade_f = Grade("Poor", 50, 100, GradeType.EXAM)
        course_f = Course("Test", 3.0)
        course_f.add_grade(grade_f)
        self.assertEqual(course_f.letter_grade(), "F")
    
    def test_grade_points(self):
        """Test grade points calculation."""
        # A grade = 4.0 points
        grade_a = Grade("Excellent", 95, 100, GradeType.EXAM)
        course_a = Course("Test", 3.0)
        course_a.add_grade(grade_a)
        self.assertEqual(course_a.grade_points(), 4.0)
        
        # F grade = 0.0 points
        grade_f = Grade("Poor", 50, 100, GradeType.EXAM)
        course_f = Course("Test", 3.0)
        course_f.add_grade(grade_f)
        self.assertEqual(course_f.grade_points(), 0.0)
    
    def test_what_if_grade(self):
        """Test what-if grade calculation."""
        self.course.add_grade(self.hw1)  # 85/100
        
        # Current: 85/100 = 85%
        # What if we add 95/100? New total: 180/200 = 90%
        hypothetical = Grade("Future HW", 95, 100, GradeType.HOMEWORK)
        new_percentage = self.course.what_if_grade(hypothetical)
        self.assertEqual(new_percentage, 90.0)


class TestStudent(unittest.TestCase):
    """Test cases for the Student class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.student = Student("John Doe")
        
        # Create courses with grades
        self.cs101 = Course("CS101", 3.0)
        self.cs101.add_grade(Grade("HW1", 85, 100, GradeType.HOMEWORK))
        self.cs101.add_grade(Grade("Exam1", 90, 100, GradeType.EXAM))
        
        self.math101 = Course("MATH101", 4.0)
        self.math101.add_grade(Grade("HW1", 95, 100, GradeType.HOMEWORK))
        self.math101.add_grade(Grade("Exam1", 88, 100, GradeType.EXAM))
    
    def test_student_creation(self):
        """Test basic student creation."""
        self.assertEqual(self.student.name, "John Doe")
        self.assertEqual(len(self.student.courses), 0)
    
    def test_add_remove_courses(self):
        """Test adding and removing courses."""
        self.student.add_course(self.cs101)
        self.assertEqual(len(self.student.courses), 1)
        self.assertIn("CS101", self.student.courses)
        
        self.student.add_course(self.math101)
        self.assertEqual(len(self.student.courses), 2)
        
        self.student.remove_course("CS101")
        self.assertEqual(len(self.student.courses), 1)
        self.assertNotIn("CS101", self.student.courses)
    
    def test_gpa_calculation(self):
        """Test GPA calculation across multiple courses."""
        self.student.add_course(self.cs101)
        self.student.add_course(self.math101)
        
        # CS101: 175/200 = 87.5% = B+ = 3.3 points * 3 credits = 9.9
        # MATH101: 183/200 = 91.5% = A- = 3.7 points * 4 credits = 14.8
        # Total: 24.7 points / 7 credits = 3.53 GPA
        
        gpa = self.student.calculate_gpa()
        self.assertAlmostEqual(gpa, 3.53, places=2)
    
    def test_empty_student_gpa(self):
        """Test GPA calculation with no courses."""
        self.assertEqual(self.student.calculate_gpa(), 0.0)
    
    def test_what_if_course_grade(self):
        """Test what-if calculation for student GPA."""
        self.student.add_course(self.cs101)
        self.student.add_course(self.math101)
        
        current_gpa = self.student.calculate_gpa()
        
        # Add hypothetical grade to CS101
        hypothetical = Grade("Final Exam", 100, 100, GradeType.EXAM)
        new_gpa = self.student.what_if_course_grade("CS101", hypothetical)
        
        self.assertIsNotNone(new_gpa)
        self.assertGreater(new_gpa, current_gpa)  # Should improve GPA
    
    def test_what_if_nonexistent_course(self):
        """Test what-if calculation for non-existent course."""
        hypothetical = Grade("Test", 100, 100, GradeType.EXAM)
        result = self.student.what_if_course_grade("NonExistent", hypothetical)
        self.assertIsNone(result)


def run_tests():
    """Run all tests and return True if all pass."""
    # Create test suite
    test_classes = [TestGrade, TestGradeCategory, TestCourse, TestStudent]
    
    suite = unittest.TestSuite()
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()