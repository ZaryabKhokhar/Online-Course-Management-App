class Assignment:
    def __init__(self, assignment_id, course_id, title, description, due_date):
        self.assignment_id = assignment_id
        self.course_id = course_id
        self.title = title
        self.description = description
        self.due_date = due_date

    def __str__(self):
        return f"Assignment(ID: {self.assignment_id}, Title: {self.title})"

class Submission:
    def __init__(self, submission_id, assignment_id, student_id, submission_date, content_path, grade=None):
        self.submission_id = submission_id
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.submission_date = submission_date
        self.content_path = content_path # Path to submitted file
        self.grade = grade

    def __str__(self):
        return f"Submission(ID: {self.submission_id}, Assignment: {self.assignment_id}, Student: {self.student_id})"