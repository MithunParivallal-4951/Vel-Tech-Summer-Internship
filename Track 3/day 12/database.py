import sqlite3

# Connect to (or create) the database file
connection = sqlite3.connect("students.db")
cursor = connection.cursor()

# Create the Students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_number TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL,
    year TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    gender TEXT NOT NULL,
    address TEXT NOT NULL
)
""")

# Sample student records
students = [
    ("Arun Kumar", "CS101", "Computer Science", "1st Year", "arun.kumar@example.com", "9876543210", "Male", "12 Gandhi Street, Chennai"),
    ("Priya Sharma", "CS102", "Computer Science", "2nd Year", "priya.sharma@example.com", "9876543211", "Female", "45 Anna Nagar, Chennai"),
    ("Mohammed Ali", "EC101", "Electronics", "1st Year", "mohammed.ali@example.com", "9876543212", "Male", "7 Park Avenue, Coimbatore"),
    ("Sneha Reddy", "EC102", "Electronics", "3rd Year", "sneha.reddy@example.com", "9876543213", "Female", "23 Lake View Road, Hyderabad"),
    ("Karthik Raj", "ME101", "Mechanical", "2nd Year", "karthik.raj@example.com", "9876543214", "Male", "56 Main Road, Madurai"),
    ("Divya Nair", "ME102", "Mechanical", "1st Year", "divya.nair@example.com", "9876543215", "Female", "9 Marine Drive, Kochi"),
    ("Rahul Verma", "IT101", "Information Technology", "4th Year", "rahul.verma@example.com", "9876543216", "Male", "18 MG Road, Bangalore"),
    ("Anjali Singh", "IT102", "Information Technology", "2nd Year", "anjali.singh@example.com", "9876543217", "Female", "31 Civil Lines, Delhi"),
    ("Vikram Joshi", "CE101", "Civil Engineering", "3rd Year", "vikram.joshi@example.com", "9876543218", "Male", "64 River Side, Pune"),
    ("Lakshmi Iyer", "CE102", "Civil Engineering", "1st Year", "lakshmi.iyer@example.com", "9876543219", "Female", "27 Temple Street, Trichy"),
]

cursor.executemany("""
INSERT OR IGNORE INTO Students
(name, roll_number, department, year, email, phone, gender, address)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", students)

connection.commit()
connection.close()

print("Database 'students.db' created successfully with sample records!")
