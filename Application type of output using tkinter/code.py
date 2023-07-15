import tkinter as tk
from tkinter import messagebox
from queue import Queue

# Define the UserManagementSystem class
class UserManagementSystem:
    def _init_(self):
        self.logged_in_user = None
        self.user_accounts = {}

    def create_account(self, username, password):
        if username not in self.user_accounts:
            self.user_accounts[username] = password
            return True
        return False

    def login(self, username, password):
        if username in self.user_accounts and self.user_accounts[username] == password:
            self.logged_in_user = username
            return True
        return False

    def logout(self):
        self.logged_in_user = None

# Create an instance of UserManagementSystem
ums = UserManagementSystem()

# Create a queue for enrollments
enrollments_queue = Queue()

# Create the main application window
root = tk.Tk()
root.title("Course Management System")

# Create the main menu
def main_menu():
    main_menu_window = tk.Toplevel(root)
    main_menu_window.title("Main Menu")

    def create_account():
        def submit():
            username = username_entry.get()
            password = password_entry.get()

            if ums.create_account(username, password):
                messagebox.showinfo("Success", "Account created successfully.")
                create_account_window.destroy()
            else:
                messagebox.showerror("Error", "Username already exists. Please choose a different username.")

        create_account_window = tk.Toplevel(main_menu_window)
        create_account_window.title("Create Account")

        username_label = tk.Label(create_account_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(create_account_window)
        username_entry.pack()

        password_label = tk.Label(create_account_window, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(create_account_window, show="*")
        password_entry.pack()

        submit_button = tk.Button(create_account_window, text="Submit", command=submit)
        submit_button.pack()

    def login():
        def submit():
            username = username_entry.get()
            password = password_entry.get()

            if ums.login(username, password):
                messagebox.showinfo("Success", "Login successful.")
                login_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid username or password.")

        login_window = tk.Toplevel(main_menu_window)
        login_window.title("Login")

        username_label = tk.Label(login_window, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(login_window)
        username_entry.pack()

        password_label = tk.Label(login_window, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(login_window, show="*")
        password_entry.pack()

        submit_button = tk.Button(login_window, text="Submit", command=submit)
        submit_button.pack()

    def rate_course():
        if ums.logged_in_user:
            def submit():
                course_to_rate = course_entry.get()
                rating = rating_entry.get()

                # Save the course rating
                messagebox.showinfo("Success", "Course rated successfully.")
                rate_course_window.destroy()
            rate_course_window = tk.Toplevel(main_menu_window)
            rate_course_window.title("Rate a Course")

            course_label = tk.Label(rate_course_window, text="Course:")
            course_label.pack()
            course_entry = tk.Entry(rate_course_window)
            course_entry.pack()

            rating_label = tk.Label(rate_course_window, text="Rating:")
            rating_label.pack()
            rating_entry = tk.Entry(rate_course_window)
            rating_entry.pack()

            submit_button = tk.Button(rate_course_window, text="Submit", command=submit)
            submit_button.pack()
        else:
            messagebox.showerror("Error", "Please login first.")

    def add_review():
        if ums.logged_in_user:
            def submit():
                course_to_review = course_entry.get()
                review_text = review_text_entry.get("1.0", tk.END)

                # Save the course review
                messagebox.showinfo("Success", "Review added successfully.")
                add_review_window.destroy()
            add_review_window = tk.Toplevel(main_menu_window)
            add_review_window.title("Add a Review")

            course_label = tk.Label(add_review_window, text="Course:")
            course_label.pack()
            course_entry = tk.Entry(add_review_window)
            course_entry.pack()

            review_text_label = tk.Label(add_review_window, text="Review:")
            review_text_label.pack()
            review_text_entry = tk.Text(add_review_window, height=5, width=30)
            review_text_entry.pack()

            submit_button = tk.Button(add_review_window, text="Submit", command=submit)
            submit_button.pack()
        else:
            messagebox.showerror("Error", "Please login first.")

    def get_course_reviews():
        def submit():
            course_to_check = course_entry.get()
            reviews = ums.get_reviews(course_to_check)
            if reviews:
                messagebox.showinfo("Course Reviews", f"Reviews for {course_to_check}:\n\n" +
                                    "\n".join(reviews))
            else:
                messagebox.showinfo("Course Reviews", f"No reviews found for {course_to_check}.")

        reviews_window = tk.Toplevel(main_menu_window)
        reviews_window.title("Get Course Reviews")

        course_label = tk.Label(reviews_window, text="Course:")
        course_label.pack()
        course_entry = tk.Entry(reviews_window)
        course_entry.pack()

        submit_button = tk.Button(reviews_window, text="Submit", command=submit)
        submit_button.pack()

    def display_enrollments():
        enrollments_window = tk.Toplevel(main_menu_window)
        enrollments_window.title("All Enrollments")

        enrollments_text = tk.Text(enrollments_window, height=10, width=50)
        enrollments_text.pack()

        enrollments_text.insert(tk.END, "Enrollments:\n\n")

        while not enrollments_queue.empty():
            enrollment = enrollments_queue.get()
            enrollments_text.insert(tk.END, f"User: {enrollment[0]} - Course: {enrollment[1]}\n")

    def enroll_course():
        if ums.logged_in_user:
            def submit():
                course_to_enroll = course_entry.get()
                enrollments_queue.put((ums.logged_in_user, course_to_enroll))
                messagebox.showinfo("Success", "Course enrollment successful.")
                enroll_course_window.destroy()

            enroll_course_window = tk.Toplevel(main_menu_window)
            enroll_course_window.title("Enroll in a Course")

            course_label = tk.Label(enroll_course_window, text="Course:")
            course_label.pack()
            course_entry = tk.Entry(enroll_course_window)
            course_entry.pack()

            submit_button = tk.Button(enroll_course_window, text="Submit", command=submit)
            submit_button.pack()
        else:
            messagebox.showerror("Error", "Please login first.")

    def get_course_recommendations():
        def submit():
            subject = subject_entry.get()
            level = level_entry.get()

            recommendations = ums.get_recommendations(subject, level)
            if recommendations:
                messagebox.showinfo("Course Recommendations", f"Recommended courses for {subject} - Level {level}:\n\n" +
                                    "\n".join(recommendations))
            else:
                messagebox.showinfo("Course Recommendations", f"No recommendations found for {subject} - Level {level}.")

        recommendations_window = tk.Toplevel(main_menu_window)
        recommendations_window.title("Get Course Recommendations")

        subject_label = tk.Label(recommendations_window, text="Subject:")
        subject_label.pack()
        subject_entry = tk.Entry(recommendations_window)
        subject_entry.pack()

        level_label = tk.Label(recommendations_window, text="Level:")
        level_label.pack()
        level_entry = tk.Entry(recommendations_window)
        level_entry.pack()

        submit_button = tk.Button(recommendations_window, text="Submit", command=submit)
        submit_button.pack()

    create_account_button = tk.Button(main_menu_window, text="Create Account", command=create_account)
    create_account_button.pack()

    login_button = tk.Button(main_menu_window, text="Login", command=login)
    login_button.pack()

    rate_course_button = tk.Button(main_menu_window, text="Rate a Course", command=rate_course)
    rate_course_button.pack()

    add_review_button = tk.Button(main_menu_window, text="Add a Review", command=add_review)
    add_review_button.pack()

    get_course_reviews_button = tk.Button(main_menu_window, text="Get Course Reviews", command=get_course_reviews)
    get_course_reviews_button.pack()

    display_enrollments_button = tk.Button(main_menu_window, text="Display All Enrollments", command=display_enrollments)
    display_enrollments_button.pack()

    enroll_course_button = tk.Button(main_menu_window, text="Enroll in a Course", command=enroll_course)
    enroll_course_button.pack()

    get_course_recommendations_button = tk.Button(main_menu_window, text="Get Course Recommendations",
                                                 command=get_course_recommendations)
    get_course_recommendations_button.pack()

# Run the main menu
main_menu()

# Run the main tkinter event loop
root.mainloop()