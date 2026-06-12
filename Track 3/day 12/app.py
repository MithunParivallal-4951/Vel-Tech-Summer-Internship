from flask import Flask, render_template

app = Flask(__name__)

# ---------------------------------------------------------
# Dummy student records (no database yet — added on Day 2)
# ---------------------------------------------------------
students = [
    {"roll": 101, "name": "Arjun Kumar",     "department": "IT",   "year": 3, "email": "arjun.kumar@example.com"},
    {"roll": 102, "name": "Priya Sharma",    "department": "CSE",  "year": 2, "email": "priya.sharma@example.com"},
    {"roll": 103, "name": "Karthik Raja",    "department": "ECE",  "year": 1, "email": "karthik.raja@example.com"},
    {"roll": 104, "name": "Divya Lakshmi",   "department": "IT",   "year": 4, "email": "divya.lakshmi@example.com"},
    {"roll": 105, "name": "Mohammed Imran",  "department": "MECH", "year": 2, "email": "mohammed.imran@example.com"},
    {"roll": 106, "name": "Sneha Reddy",     "department": "CSE",  "year": 3, "email": "sneha.reddy@example.com"},
    {"roll": 107, "name": "Vignesh Pillai",  "department": "EEE",  "year": 1, "email": "vignesh.pillai@example.com"},
    {"roll": 108, "name": "Anitha Suresh",   "department": "IT",   "year": 2, "email": "anitha.suresh@example.com"},
    {"roll": 109, "name": "Rahul Verma",     "department": "CSE",  "year": 4, "email": "rahul.verma@example.com"},
    {"roll": 110, "name": "Lakshmi Narayan", "department": "ECE",  "year": 3, "email": "lakshmi.narayan@example.com"},
    {"roll": 111, "name": "Sanjay Gupta",    "department": "MECH", "year": 1, "email": "sanjay.gupta@example.com"},
    {"roll": 112, "name": "Meena Iyer",      "department": "IT",   "year": 3, "email": "meena.iyer@example.com"},
]


@app.route("/")
def home():
    return render_template("index.html", active_page="home", student_count=len(students))


@app.route("/register")
def register():
    return render_template("register.html", active_page="register")


@app.route("/students")
def student_list():
    return render_template("students.html", active_page="students", students=students)


@app.route("/about")
def about():
    return render_template("about.html", active_page="about")


if __name__ == "__main__":
    app.run(debug=True)
