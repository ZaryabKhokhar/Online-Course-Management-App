class Grade:
    def __init__(self, grade_id, student_id, course_id, assignment_id, grade_value, comments=""):
        self.grade_id = grade_id
        self.student_id = student_id
        self.course_id = course_id
        self.assignment_id = assignment_id
        self.grade_value = grade_value # e.g., A, B, C or 85/100
        self.comments = comments

    def __str__(self):
        return f"Grade(ID: {self.grade_id}, Student: {self.student_id}, Course: {self.course_id}, Grade: {self.grade_value})"