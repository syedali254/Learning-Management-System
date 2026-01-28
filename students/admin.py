

# Register your models here.
from django.contrib import admin
from students.models import Instructor, students_l, Course, Enrollment

admin.site.register(Instructor)
admin.site.register(students_l)
admin.site.register(Course)
admin.site.register(Enrollment)