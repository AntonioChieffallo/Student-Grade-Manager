# Student Grade Manager

A comprehensive Python application for students to manage their grades across multiple courses and calculate their GPA. This tool allows students to track homework, exam, and quiz grades, calculate course totals, and perform "what-if" scenarios to see how future grades might affect their overall performance.

## Features

- **Grade Management**: Track homework, exam, and quiz grades with points earned and total points possible
- **Course Management**: Manage multiple courses with different credit hours
- **Automatic Calculations**: 
  - Individual assignment percentages
  - Category totals (homework, exams, quizzes)
  - Overall course percentages and letter grades
  - GPA calculation across all courses
- **What-If Calculator**: See how hypothetical grades would affect your course grade and GPA
- **User-Friendly CLI**: Interactive command-line interface for easy grade entry and viewing

## Installation

No additional dependencies required! This application uses only Python's standard library.

```bash
git clone https://github.com/AntonioChieffallo/Student-Grade-Manager.git
cd Student-Grade-Manager
```

## Usage

### Running the Application

```bash
python main.py
```

### Command-Line Interface

The application provides an interactive menu with the following options:

1. **Add new course** - Create a new course with credit hours
2. **Add grade to existing course** - Add homework, exam, or quiz grades
3. **View grades and course details** - See detailed grade breakdown
4. **View GPA** - Display current GPA and course summary
5. **What-if grade calculator** - Calculate impact of hypothetical grades
6. **Remove course** - Remove a course from your records
7. **Exit** - Close the application

### Example Usage

```
Enter your name: John Doe

MAIN MENU
1. Add new course
2. Add grade to existing course
3. View grades and course details
4. View GPA
5. What-if grade calculator
6. Remove course
7. Exit

Enter your choice: 1
Enter course name: Computer Science 101
Enter credit hours (default: 3.0): 3
Course 'Computer Science 101' added successfully!
```

## Grade Categories

The system supports three types of grades:

- **Homework**: Regular assignments and projects
- **Exam**: Midterms, finals, and major tests  
- **Quiz**: Short assessments and pop quizzes

## GPA Calculation

The system uses a standard 4.0 GPA scale:

| Letter Grade | Grade Points |
|-------------|-------------|
| A+ / A      | 4.0         |
| A-          | 3.7         |
| B+          | 3.3         |
| B           | 3.0         |
| B-          | 2.7         |
| C+          | 2.3         |
| C           | 2.0         |
| C-          | 1.7         |
| D+          | 1.3         |
| D           | 1.0         |
| D-          | 0.7         |
| F           | 0.0         |

GPA is calculated as: (Sum of grade points × credit hours) ÷ Total credit hours

## What-If Calculator

The what-if calculator allows you to:
- See how a hypothetical assignment would affect your course percentage
- Understand the impact on your letter grade
- Calculate how it would change your overall GPA

## Running Tests

The application includes comprehensive unit tests:

```bash
python test_grade_manager.py
```

## Code Structure

- `grade.py` - Core classes (Grade, GradeCategory, Course, Student)
- `main.py` - Command-line interface
- `test_grade_manager.py` - Unit tests

## Example Output

```
Student: John Doe
GPA: 3.40

Course: Computer Science 101 (3.0 credit hours)
Overall: 271/320 (84.69%) - B

Homework: 175/200 (87.50%)
  - HW1: 85/100 (85.00%)
  - HW2: 90/100 (90.00%)

Exam: 78/100 (78.00%)
  - Midterm Exam: 78/100 (78.00%)

Quiz: 18/20 (90.00%)
  - Quiz1: 18/20 (90.00%)
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.