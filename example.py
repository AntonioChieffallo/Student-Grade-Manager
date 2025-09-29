#!/usr/bin/env python3
"""
Example usage of the Student Grade Manager classes.
This demonstrates how to use the grade management system programmatically.
"""

from grade import Student, Course, Grade, GradeType


def main():
    """Demonstrate the grade management system."""
    print("=" * 60)
    print("STUDENT GRADE MANAGER - EXAMPLE USAGE")
    print("=" * 60)
    
    # Create a student
    student = Student("Alice Johnson")
    
    # Create and populate Computer Science course
    cs_course = Course("Computer Science 101", 3.0)
    
    # Add homework grades
    cs_course.add_grade(Grade("HW1: Variables and Data Types", 85, 100, GradeType.HOMEWORK))
    cs_course.add_grade(Grade("HW2: Control Structures", 92, 100, GradeType.HOMEWORK))
    cs_course.add_grade(Grade("HW3: Functions", 88, 100, GradeType.HOMEWORK))
    
    # Add exam grades
    cs_course.add_grade(Grade("Midterm Exam", 78, 100, GradeType.EXAM))
    
    # Add quiz grades
    cs_course.add_grade(Grade("Quiz 1: Syntax", 18, 20, GradeType.QUIZ))
    cs_course.add_grade(Grade("Quiz 2: Debugging", 19, 20, GradeType.QUIZ))
    
    # Create and populate Mathematics course
    math_course = Course("Calculus I", 4.0)
    
    # Add homework grades
    math_course.add_grade(Grade("HW1: Limits", 95, 100, GradeType.HOMEWORK))
    math_course.add_grade(Grade("HW2: Derivatives", 88, 100, GradeType.HOMEWORK))
    math_course.add_grade(Grade("HW3: Chain Rule", 91, 100, GradeType.HOMEWORK))
    
    # Add exam grades
    math_course.add_grade(Grade("Exam 1", 87, 100, GradeType.EXAM))
    math_course.add_grade(Grade("Exam 2", 93, 100, GradeType.EXAM))
    
    # Add quiz grades
    math_course.add_grade(Grade("Quiz 1", 28, 30, GradeType.QUIZ))
    
    # Add courses to student
    student.add_course(cs_course)
    student.add_course(math_course)
    
    # Display complete grade report
    print(f"\n{student}")
    
    # Demonstrate what-if calculations
    print("\n" + "=" * 60)
    print("WHAT-IF SCENARIOS")
    print("=" * 60)
    
    # What if Alice gets 95/100 on her CS final exam?
    hypothetical_cs_final = Grade("Final Exam", 95, 100, GradeType.EXAM)
    current_cs_percentage = cs_course.course_percentage()
    new_cs_percentage = cs_course.what_if_grade(hypothetical_cs_final)
    
    print(f"\nCS 101 - Adding Final Exam (95/100):")
    print(f"  Current course grade: {current_cs_percentage:.2f}% ({cs_course.letter_grade()})")
    print(f"  With final exam: {new_cs_percentage:.2f}%")
    print(f"  Improvement: {new_cs_percentage - current_cs_percentage:+.2f} percentage points")
    
    # What would this do to her GPA?
    current_gpa = student.calculate_gpa()
    new_gpa = student.what_if_course_grade("Computer Science 101", hypothetical_cs_final)
    
    print(f"\nGPA Impact:")
    print(f"  Current GPA: {current_gpa:.2f}")
    print(f"  GPA with CS final: {new_gpa:.2f}")
    print(f"  GPA change: {new_gpa - current_gpa:+.2f}")
    
    # What if she gets a perfect score on a Math quiz?
    hypothetical_math_quiz = Grade("Quiz 2", 30, 30, GradeType.QUIZ)
    current_math_percentage = math_course.course_percentage()
    new_math_percentage = math_course.what_if_grade(hypothetical_math_quiz)
    
    print(f"\nCalculus I - Adding Perfect Quiz (30/30):")
    print(f"  Current course grade: {current_math_percentage:.2f}% ({math_course.letter_grade()})")
    print(f"  With perfect quiz: {new_math_percentage:.2f}%")
    print(f"  Improvement: {new_math_percentage - current_math_percentage:+.2f} percentage points")
    
    # Demonstrate individual category breakdowns
    print("\n" + "=" * 60)
    print("DETAILED CATEGORY ANALYSIS")
    print("=" * 60)
    
    for course_name, course in student.courses.items():
        print(f"\n{course_name}:")
        for grade_type in [GradeType.HOMEWORK, GradeType.EXAM, GradeType.QUIZ]:
            category = course.categories[grade_type]
            if len(category) > 0:
                print(f"  {grade_type.value.title()}: {category.category_percentage():.1f}% "
                      f"({category.total_points_earned()}/{category.total_points_possible()} points)")
    
    print("\n" + "=" * 60)
    print("EXAMPLE COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()