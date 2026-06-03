def get_grade(marks):
    if marks >= 90:
        return 'A'
    elif marks >= 75:
        return 'B'
    elif marks >= 60:
        return 'C'
    elif marks >= 45:
        return 'D'
    else:
        return 'F'
students = [
    ("Alice", 95),
    ("Bob", 78),
    ("Charlie", 62),
    ("Diana", 48),
    ("Eve", 35),
]
for name, marks in students:
    grade = get_grade(marks)
    print(f"{name}: {marks} marks -> Grade {grade}")
