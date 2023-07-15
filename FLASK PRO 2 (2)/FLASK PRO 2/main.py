from flask import Flask, render_template, request, redirect, url_for, session
from collections import deque


app = Flask(__name__)
app.secret_key = "mysecretkey"

course_hash_table = {}
course_graph = {}
course_queue = deque()


class Course:
    def __init__(self, name, subject, level, instructor, rating):
        self.name = name
        self.subject = subject
        self.level = level
        self.instructor = instructor
        self.rating = rating


def initialize_courses():
    global course_hash_table, course_graph, course_queue

    course_database = {
        "course A": {"subject": "Mathematics", "level": "Beginner", "instructor": "Instructor A", "rating": 4.5},
        "course B": {"subject": "Science", "level": "Intermediate", "instructor": "Instructor B", "rating": 4.0},
        "course C": {"subject": "History", "level": "Advanced", "instructor": "Instructor C", "rating": 4.2},
        "course D": {"subject": "Computer Science", "level": "Intermediate", "instructor": "Instructor D", "rating": 4.8},
        "course E": {"subject": "Art", "level": "Beginner", "instructor": "Instructor E", "rating": 3.9},
        "course F": {"subject": "Languages", "level": "Advanced", "instructor": "Instructor F", "rating": 4.6}
    }

    for course_name, attributes in course_database.items():
        course = Course(course_name, attributes["subject"], attributes["level"], attributes["instructor"],
                        attributes["rating"])
        course_hash_table[course_name] = course
        course_graph[course_name] = set()
        course_queue.append(course_name)


@app.route("/", methods=["GET", "POST"])
def index():
    if "username" in session:
        username = session["username"]
        courses = []
        for course_name in course_queue:
            course = course_hash_table[course_name]
            courses.append((course.name, course.subject, course.level, course.instructor, course.rating))
        return render_template("index.html", ums={"logged_in_user": username}, courses=courses)
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            error = "Invalid username or password."
            return render_template("signup.html", error=error)
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            error = "Invalid username or password."
            return render_template("login.html", error=error)
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/add_course", methods=["POST"])
def add_course():
    if "username" in session:
        username = session["username"]
        course_name = request.form.get("name")
        subject = request.form.get("subject")
        level = request.form.get("level")
        instructor = request.form.get("instructor")
        rating = float(request.form.get("rating"))

        if course_name and subject and level and instructor and rating:
            course = Course(course_name, subject, level, instructor, rating)
            course_hash_table[course_name] = course
            course_graph[course_name] = set()
            course_queue.append(course_name)
        return redirect(url_for("index"))
    return redirect(url_for("login"))


if __name__ == "__main__":
    initialize_courses()
    app.run(debug=True)
