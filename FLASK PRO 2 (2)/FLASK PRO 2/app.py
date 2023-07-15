from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
db_name = "course_database.db"

# Create a connection to the SQLite database
def create_connection():
    conn = sqlite3.connect(db_name)
    return conn

# Create the courses table in the database if it doesn't exist
def create_courses_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subject TEXT NOT NULL,
        level TEXT NOT NULL,
        instructor TEXT NOT NULL,
        rating REAL NOT NULL
    )
    """
    conn.execute(query)

# Insert a course into the database
def insert_course(conn, name, subject, level, instructor, rating):
    query = """
    INSERT INTO courses (name, subject, level, instructor, rating)
    VALUES (?, ?, ?, ?, ?)
    """
    conn.execute(query, (name, subject, level, instructor, rating))
    conn.commit()

# Get all courses from the database
def get_all_courses(conn):
    query = """
    SELECT name, subject, level, instructor, rating FROM courses
    """
    cursor = conn.execute(query)
    courses = cursor.fetchall()
    return courses

# User management system
class UserManagementSystem:
    def __init__(self):
        self.users = []
        self.logged_in_user = None  # Track the logged-in user

    def create_account(self, username, password):
        self.users.append((username, password))

    def login(self, username, password):
        for user in self.users:
            if user[0] == username and user[1] == password:
                self.logged_in_user = user[0]  # Set the logged-in user
                return True
        return False

    def logout(self):
        self.logged_in_user = None

# Create an instance of the UserManagementSystem
ums = UserManagementSystem()

@app.route("/")
def index():
    conn = create_connection()
    create_courses_table(conn)
    courses = get_all_courses(conn)
    conn.close()
    return render_template("index.html", courses=courses, ums=ums)


@app.route("/add_course", methods=["POST"])
def add_course():
    name = request.form["name"]
    subject = request.form["subject"]
    level = request.form["level"]
    instructor = request.form["instructor"]
    rating = float(request.form["rating"])

    conn = create_connection()
    insert_course(conn, name, subject, level, instructor, rating)
    conn.close()
    return redirect(url_for("index"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        ums.create_account(username, password)
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if ums.login(username, password):
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")


@app.route("/logout")
def logout():
    ums.logout()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
