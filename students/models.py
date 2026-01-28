from django.db import models
from django.contrib.auth.models import User

class students_l(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    expertise = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(students_l, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"





ATTENDANCE_STATUS = (
    ('P', 'Present'),
    ('A', 'Absent'),
    ('L', 'Leave'),
)


class Attendance(models.Model):
    student = models.ForeignKey('students_l', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    status = models.CharField(max_length=1, choices=ATTENDANCE_STATUS)

    class Meta:
        unique_together = ('student', 'course', 'date')  # Prevent duplicate entries
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title} - {self.date} ({self.status})"

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='course_materials/')  # uploaded files go to /media/course_materials/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

from django.utils import timezone

class Notification(models.Model):
    student = models.ForeignKey(students_l, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)


class Assignments(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    deadline = models.DateTimeField()  #✅ (Correct)

    file=models.FileField(upload_to='assignments/')
    created_at=models.DateTimeField(auto_now_add=True)

class Submissions(models.Model):
    student=models.ForeignKey(students_l,on_delete=models.CASCADE)
    assignment=models.ForeignKey(Assignments,on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_late = models.BooleanField()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

