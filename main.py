#!/usr/bin/env python3
"""
Student Grade Manager - Command Line Interface
A tool for students to manage their grades across multiple courses and calculate GPA.
"""

import sys
from typing import Optional
from grade import Student, Course, Grade, GradeType


class GradeManagerCLI:
    """Command-line interface for the Grade Manager."""
    
    def __init__(self):
        self.student: Optional[Student] = None
    
    def run(self):
        """Main program loop."""
        print("=" * 60)
        print("          STUDENT GRADE MANAGER")
        print("=" * 60)
        print()
        
        # Get student name
        name = input("Enter your name: ").strip()
        if not name:
            print("Name cannot be empty. Exiting.")
            return
        
        self.student = Student(name)
        print(f"\nWelcome, {name}!")
        
        while True:
            self.show_main_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.add_course()
            elif choice == '2':
                self.add_grade()
            elif choice == '3':
                self.view_grades()
            elif choice == '4':
                self.view_gpa()
            elif choice == '5':
                self.what_if_calculator()
            elif choice == '6':
                self.remove_course()
            elif choice == '7':
                print("\nThank you for using Student Grade Manager!")
                break
            else:
                print("\nInvalid choice. Please try again.")
    
    def show_main_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 40)
        print("MAIN MENU")
        print("=" * 40)
        print("1. Add new course")
        print("2. Add grade to existing course")
        print("3. View grades and course details")
        print("4. View GPA")
        print("5. What-if grade calculator")
        print("6. Remove course")
        print("7. Exit")
    
    def add_course(self):
        """Add a new course."""
        print("\n--- ADD NEW COURSE ---")
        course_name = input("Enter course name: ").strip()
        if not course_name:
            print("Course name cannot be empty.")
            return
        
        if course_name in self.student.courses:
            print(f"Course '{course_name}' already exists.")
            return
        
        while True:
            try:
                credit_hours = float(input("Enter credit hours (default: 3.0): ").strip() or "3.0")
                if credit_hours <= 0:
                    print("Credit hours must be positive.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number for credit hours.")
        
        course = Course(course_name, credit_hours)
        self.student.add_course(course)
        print(f"Course '{course_name}' added successfully!")
    
    def add_grade(self):
        """Add a grade to an existing course."""
        if not self.student.courses:
            print("\nNo courses available. Please add a course first.")
            return
        
        print("\n--- ADD GRADE ---")
        
        # Show available courses
        print("Available courses:")
        course_names = list(self.student.courses.keys())
        for i, name in enumerate(course_names, 1):
            print(f"{i}. {name}")
        
        # Select course
        while True:
            try:
                choice = int(input(f"Select course (1-{len(course_names)}): "))
                if 1 <= choice <= len(course_names):
                    course_name = course_names[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(course_names)}.")
            except ValueError:
                print("Please enter a valid number.")
        
        course = self.student.courses[course_name]
        
        # Get assignment details
        assignment_name = input("Enter assignment name: ").strip()
        if not assignment_name:
            print("Assignment name cannot be empty.")
            return
        
        # Select grade type
        print("\nGrade types:")
        print("1. Homework")
        print("2. Exam")
        print("3. Quiz")
        
        while True:
            try:
                type_choice = int(input("Select grade type (1-3): "))
                if type_choice == 1:
                    grade_type = GradeType.HOMEWORK
                    break
                elif type_choice == 2:
                    grade_type = GradeType.EXAM
                    break
                elif type_choice == 3:
                    grade_type = GradeType.QUIZ
                    break
                else:
                    print("Please enter 1, 2, or 3.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get score and total points
        while True:
            try:
                score = float(input("Enter points earned: "))
                if score < 0:
                    print("Points earned cannot be negative.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number for points earned.")
        
        while True:
            try:
                total_points = float(input("Enter total points possible: "))
                if total_points <= 0:
                    print("Total points must be positive.")
                    continue
                if score > total_points:
                    print("Points earned cannot exceed total points.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number for total points.")
        
        # Create and add the grade
        try:
            grade = Grade(assignment_name, score, total_points, grade_type)
            course.add_grade(grade)
            print(f"\nGrade added successfully!")
            print(f"{assignment_name}: {score}/{total_points} ({grade.percentage:.2f}%)")
        except ValueError as e:
            print(f"Error adding grade: {e}")
    
    def view_grades(self):
        """View all grades and course details."""
        if not self.student.courses:
            print("\nNo courses available.")
            return
        
        print("\n" + "=" * 60)
        print("GRADE REPORT")
        print("=" * 60)
        print(str(self.student))
    
    def view_gpa(self):
        """View current GPA."""
        gpa = self.student.calculate_gpa()
        print(f"\n--- GPA SUMMARY ---")
        print(f"Student: {self.student.name}")
        print(f"Current GPA: {gpa:.2f}")
        
        if self.student.courses:
            print("\nCourse Breakdown:")
            for course in self.student.courses.values():
                if course.total_points_possible() > 0:
                    print(f"  {course.name}: {course.course_percentage():.2f}% ({course.letter_grade()}) - {course.credit_hours} credits")
                else:
                    print(f"  {course.name}: No grades yet - {course.credit_hours} credits")
    
    def what_if_calculator(self):
        """Calculate what-if scenarios for grades."""
        if not self.student.courses:
            print("\nNo courses available. Please add a course first.")
            return
        
        print("\n--- WHAT-IF GRADE CALCULATOR ---")
        print("Calculate how a hypothetical grade would affect your course grade or GPA.")
        
        # Show available courses
        print("\nAvailable courses:")
        course_names = list(self.student.courses.keys())
        for i, name in enumerate(course_names, 1):
            course = self.student.courses[name]
            print(f"{i}. {course.name} (Current: {course.course_percentage():.2f}% - {course.letter_grade()})")
        
        # Select course
        while True:
            try:
                choice = int(input(f"\nSelect course (1-{len(course_names)}): "))
                if 1 <= choice <= len(course_names):
                    course_name = course_names[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(course_names)}.")
            except ValueError:
                print("Please enter a valid number.")
        
        course = self.student.courses[course_name]
        
        # Get hypothetical assignment details
        assignment_name = input("Enter hypothetical assignment name: ").strip() or "Hypothetical Assignment"
        
        # Select grade type
        print("\nGrade types:")
        print("1. Homework")
        print("2. Exam")
        print("3. Quiz")
        
        while True:
            try:
                type_choice = int(input("Select grade type (1-3): "))
                if type_choice == 1:
                    grade_type = GradeType.HOMEWORK
                    break
                elif type_choice == 2:
                    grade_type = GradeType.EXAM
                    break
                elif type_choice == 3:
                    grade_type = GradeType.QUIZ
                    break
                else:
                    print("Please enter 1, 2, or 3.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get hypothetical score and total points
        while True:
            try:
                score = float(input("Enter hypothetical points earned: "))
                if score < 0:
                    print("Points earned cannot be negative.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number for points earned.")
        
        while True:
            try:
                total_points = float(input("Enter total points possible: "))
                if total_points <= 0:
                    print("Total points must be positive.")
                    continue
                if score > total_points:
                    print("Points earned cannot exceed total points.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number for total points.")
        
        # Calculate what-if scenarios
        try:
            hypothetical_grade = Grade(assignment_name, score, total_points, grade_type)
            
            # Course-level what-if
            current_percentage = course.course_percentage()
            new_percentage = course.what_if_grade(hypothetical_grade)
            
            # GPA-level what-if
            current_gpa = self.student.calculate_gpa()
            new_gpa = self.student.what_if_course_grade(course_name, hypothetical_grade)
            
            print(f"\n--- WHAT-IF RESULTS ---")
            print(f"Hypothetical Assignment: {assignment_name}")
            print(f"Score: {score}/{total_points} ({hypothetical_grade.percentage:.2f}%)")
            print()
            print(f"Course Impact ({course_name}):")
            print(f"  Current: {current_percentage:.2f}% ({course.letter_grade()})")
            print(f"  With new grade: {new_percentage:.2f}%")
            
            # Calculate what the new letter grade would be
            temp_course = Course(course.name, course.credit_hours)
            for category in course.categories.values():
                for grade in category.grades:
                    temp_course.add_grade(grade)
            temp_course.add_grade(hypothetical_grade)
            new_letter_grade = temp_course.letter_grade()
            
            print(f"  New letter grade: {new_letter_grade}")
            print(f"  Change: {new_percentage - current_percentage:+.2f} percentage points")
            print()
            print(f"GPA Impact:")
            print(f"  Current GPA: {current_gpa:.2f}")
            if new_gpa is not None:
                print(f"  New GPA: {new_gpa:.2f}")
                print(f"  Change: {new_gpa - current_gpa:+.2f} points")
            
        except ValueError as e:
            print(f"Error in calculation: {e}")
    
    def remove_course(self):
        """Remove a course."""
        if not self.student.courses:
            print("\nNo courses available.")
            return
        
        print("\n--- REMOVE COURSE ---")
        print("Available courses:")
        course_names = list(self.student.courses.keys())
        for i, name in enumerate(course_names, 1):
            print(f"{i}. {name}")
        
        while True:
            try:
                choice = int(input(f"Select course to remove (1-{len(course_names)}): "))
                if 1 <= choice <= len(course_names):
                    course_name = course_names[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(course_names)}.")
            except ValueError:
                print("Please enter a valid number.")
        
        confirm = input(f"Are you sure you want to remove '{course_name}'? (y/N): ").strip().lower()
        if confirm == 'y' or confirm == 'yes':
            self.student.remove_course(course_name)
            print(f"Course '{course_name}' removed successfully!")
        else:
            print("Course removal cancelled.")


def main():
    """Main entry point."""
    try:
        cli = GradeManagerCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()