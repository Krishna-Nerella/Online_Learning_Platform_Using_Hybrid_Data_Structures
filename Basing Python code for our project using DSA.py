import time

course_database = {
    "Course A": {"subject": "Mathematics", "level": "Beginner", "instructor": "Instructor A", "rating": 4.5},
    "Course B": {"subject": "Science", "level": "Intermediate", "instructor": "Instructor B", "rating": 4.0},
    "Course C": {"subject": "History", "level": "Advanced", "instructor": "Instructor C", "rating": 4.2},
    "Course D": {"subject": "Computer Science", "level": "Intermediate", "instructor": "Instructor D", "rating": 4.8},
    "Course E": {"subject": "Art", "level": "Beginner", "instructor": "Instructor E", "rating": 3.9},
    "Course F": {"subject": "Languages", "level": "Advanced", "instructor": "Instructor F", "rating": 4.6}
}

# Graph class to represent course connections
class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, course, subject, level):
        key = subject + '_' + level
        if key in self.graph:
            self.graph[key].append(course)
        else:
            self.graph[key] = [course]

# Hash Table class to store course attributes and ratings
class HashTable:
    def __init__(self):
        self.table = {}

    def insert(self, key, value):
        self.table[key] = value

    def get(self, key):
        return self.table.get(key)

# Queue class to represent course enrollment
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, course):
        self.queue.append(course)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

    def display(self):
        if not self.is_empty():
            print("Enrollment List:")
            for course in self.queue:
                print(course)
        else:
            print("Enrollment list is empty.")

# Build the graph and hash tables
course_graph = Graph()
course_attributes = HashTable()
course_ratings = HashTable()
course_reviews = HashTable()

for course, attributes in course_database.items():
    subject = attributes["subject"]
    level = attributes["level"]
    course_graph.add_edge(course, subject, level)
    course_attributes.insert(course, attributes)

# Perform personalized course recommendations based on subject and level
def recommend_courses(subject, level):
    key = subject + '_' + level
    recommended_courses = []

    # Find courses of the given subject and level in the graph
    if key in course_graph.graph:
        courses = course_graph.graph[key]
        # Retrieve course attributes
        for course in courses:
            attributes = course_attributes.get(course)
            if attributes:
                recommended_courses.append((course, attributes["instructor"]))

    return recommended_courses

# User management system
class UserManagementSystem:
    def __init__(self):
        self.users = []
        self.ratings = HashTable()
        self.reviews = HashTable()
        self.enrollment_list = Queue()
        self.logged_in_user = None  # Track the logged-in user

    def create_account(self):
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        self.users.append((username, password))
        print("Account created successfully.")

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        for user in self.users:
            if user[0] == username and user[1] == password:
                self.logged_in_user = user[0]  # Set the logged-in user
                print("Login successful.")
                return True

        print("Invalid username or password.")
        return False

    def rate_course(self, course):
        rating = input(f"Rate the course '{course}': ")
        self.ratings.insert(course, rating)
        print("Course rated successfully.")

    def add_review(self, course, review):
        if course in self.reviews.table:
            self.reviews.table[course].append(review)
        else:
            self.reviews.table[course] = [review]

    def get_course_reviews(self, course):
        reviews = self.reviews.get(course)
        if reviews:
            print(f"Reviews for '{course}':")
            for review in reviews:
                print(review)
        else:
            print("No reviews found for the given course.")

    def enroll_in_course(self, course):
        self.enrollment_list.enqueue(course)
        print(f"'{course}' added to the enrollment list.")

    def start_course(self):
        if not self.enrollment_list.is_empty():
            print("Starting enrolled courses:")
            while not self.enrollment_list.is_empty():
                course = self.enrollment_list.dequeue()
                print(f"Now starting course: {course}")
                time.sleep(2)  # Simulating course duration
            print("All courses completed.")
        else:
            print("No courses in the enrollment list.")

    def display_enrollment_list(self):
        self.enrollment_list.display()

# Create an instance of the UserManagementSystem
ums = UserManagementSystem()

# Menu-driven loop
while True:
    print("██████████████████████████████████████████████████████████████████████████████")
    print("█▄─▀█▀─▄█▄─▄▄─█▄─▀█▄─▄█─▄─▄─█─▄▄─█▄─▄▄▀████▀▄─██▄─▀█▄─▄█▄─▄▄▀███▄─▀█▀─▄█▄─▄▄─█")
    print("██─█▄█─███─▄█▀██─█▄▀─████─███─██─██─▄─▄████─▀─███─█▄▀─███─██─████─█▄█─███─▄█▀█")
    print("▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▀▀▄▄▄▄▀▄▄▀▄▄▀▀▀▄▄▀▄▄▀▄▄▄▀▀▄▄▀▄▄▄▄▀▀▀▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀")
    print("1. Create Account")
    print("2. Login")
    print("3. Rate a Course")
    print("4. Add a Review")
    print("5. Get Course Recommendations")
    print("6. Get Course Reviews")
    print("7. Enroll in a Course")
    print("8. Start Enrolled Courses")
    print("9. Display Enrollment List")
    print("10. Exit")
    choice = input("Enter your choice (1-10): ")

    if choice == "1":
        ums.create_account()
    elif choice == "2":
        if ums.login():
            # Get user input for subject
            print("Select a Subject:")
            print("1. Mathematics")
            print("2. Science")
            print("3. History")
            subject_choice = input("Enter your subject choice (1-3): ")

            # Get user input for level
            print("Select a Level:")
            print("1. Beginner")
            print("2. Intermediate")
            print("3. Advanced")
            level_choice = input("Enter your level choice (1-3): ")

            # Mapping subject choice
            subject_mapping = {
                "1": "Mathematics",
                "2": "Science",
                "3": "History"
            }

            # Mapping level choice
            level_mapping = {
                "1": "Beginner",
                "2": "Intermediate",
                "3": "Advanced"
            }

            # Validate and retrieve subject and level
            if subject_choice in subject_mapping and level_choice in level_mapping:
                user_subject = subject_mapping[subject_choice]
                user_level = level_mapping[level_choice]

                # Get personalized course recommendations based on subject and level
                recommendations = recommend_courses(user_subject, user_level)

                # Display the recommended courses
                if len(recommendations) > 0:
                    print(f"Recommended Courses in {user_subject} - {user_level} Level:")
                    for course, instructor in recommendations:
                        print(f"Course: {course} - Instructor: {instructor}")
                else:
                    print("No courses found based on the given subject and level.")
            else:
                print("Invalid subject or level choice. Please try again.")

    elif choice == "3":
        if ums.login():
            course_to_rate = input("Enter the name of the course you want to rate: ")
            ums.rate_course(course_to_rate)

    elif choice == "4":
        if ums.login():
            course_to_review = input("Enter the name of the course you want to review: ")
            review = input("Enter your review: ")
            ums.add_review(course_to_review, review)

    elif choice == "5":
        print("Select a Subject:")
        print("1. Mathematics")
        print("2. Science")
        print("3. History")
        subject_choice = input("Enter your subject choice (1-3): ")

        print("Select a Level:")
        print("1. Beginner")
        print("2. Intermediate")
        print("3. Advanced")
        level_choice = input("Enter your level choice (1-3): ")

        subject_mapping = {
            "1": "Mathematics",
            "2": "Science",
            "3": "History"
        }

        level_mapping = {
            "1": "Beginner",
            "2": "Intermediate",
            "3": "Advanced"
        }

        if subject_choice in subject_mapping and level_choice in level_mapping:
            user_subject = subject_mapping[subject_choice]
            user_level = level_mapping[level_choice]

            recommendations = recommend_courses(user_subject, user_level)

            if len(recommendations) > 0:
                print(f"Recommended Courses in {user_subject} - {user_level} Level:")
                for course, instructor in recommendations:
                    print(f"Course: {course} - Instructor: {instructor}")
            else:
                print("No courses found based on the given subject and level.")
        else:
            print("Invalid subject or level choice. Please try again.")

    elif choice == "6":
        course_to_check = input("Enter the name of the course you want to check reviews for: ")
        ums.get_course_reviews(course_to_check)

    elif choice == "7":
        if ums.login():
            course_to_enroll = input("Enter the name of the course you want to enroll in: ")
            ums.enroll_in_course(course_to_enroll)

    elif choice == "8":
        if ums.login():
            ums.start_course()

    elif choice == "9":
        if ums.login():
            ums.display_enrollment_list()

    elif choice == "10":
        print("Thank you for using the Course Management System. Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")
