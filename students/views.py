# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import students_l, Instructor, Course, Enrollment,Attendance,Notification,Assignments,Submissions
from datetime import datetime

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if hasattr(user, 'instructor'):
                return redirect('instructor_dashboard')
            elif hasattr(user, 'students_l'):
                return redirect('student_dashboard')
            else:
                return redirect('/admin/')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def student_dashboard(request):
    if not hasattr(request.user, 'students_l'):
        return redirect('login')
    courses = Course.objects.all()
    return render(request, "student_dashboard.html", {'courses': courses})

@login_required
def enroll(request, id):
    course = get_object_or_404(Course, id=id)
    student = request.user.students_l

    if request.method == 'POST':
        if Enrollment.objects.filter(student=student, course=course).exists():
            messages.info(request, "Already enrolled.")
        else:
            Enrollment.objects.create(student=student, course=course)
            messages.success(request, "Enrolled successfully.")
        return redirect('student_dashboard')

    return render(request, 'enroll.html', {'course': course})

@login_required
def instructor_dashboard(request):
    if not hasattr(request.user, 'instructor'):
        return redirect('login')
    instructor = request.user.instructor
    courses = Course.objects.filter(instructor=instructor)
    return render(request, 'instructor_dashboard.html', {'courses': courses})

@login_required
def add_course(request):
    if not hasattr(request.user, 'instructor'):
        return redirect('login')
    instructor = request.user.instructor

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        Course.objects.create(title=title, description=description, instructor=instructor)
        return redirect('instructor_dashboard')

    return render(request, 'add_co.html')

@login_required
def update_course(request, id):
    course = get_object_or_404(Course, id=id)
    if not hasattr(request.user, 'instructor') or course.instructor != request.user.instructor:
        return redirect('login')

    if request.method == 'POST':
        course.title = request.POST['title']
        course.description = request.POST['description']
        course.save()
        return redirect('instructor_dashboard')

    return render(request, 'update_course.html', {'course': course})


@login_required
def students_enrolled(request, id):
    course = get_object_or_404(Course, id=id)

    if not hasattr(request.user, 'instructor') or course.instructor != request.user.instructor:
        return redirect('login')

    enrollments = Enrollment.objects.filter(course=course).select_related('student__user')
    return render(request, 'students_enrolled.html', {'course': course, 'enrollments': enrollments})


@login_required
def my_courses(request):
    if not hasattr(request.user, 'students_l'):  # ❗ should check for student, not instructor
        return redirect('login')

    student = request.user.students_l
    courses = Enrollment.objects.filter(student=student)

    return render(request, 'my_courses.html', {'courses': courses})


from datetime import date


from datetime import date

@login_required
def mark_attendance(request, student_id):
    if not hasattr(request.user, 'instructor'):
        return redirect('login')

    student = get_object_or_404(students_l, id=student_id)

    
    instructor_courses = Course.objects.filter(instructor=request.user.instructor)
    enrollment = Enrollment.objects.filter(student=student, course__in=instructor_courses).first()

    if not enrollment:
        messages.error(request, "You are not authorized to mark this student's attendance.")
        return redirect('instructor_dashboard')

    if request.method == 'POST':
        date_selected = request.POST.get('date') or date.today()
        status = request.POST.get('status')

        if status in ['P', 'A', 'L']:
            Attendance.objects.update_or_create(
                student=student,
                course=enrollment.course,
                date=date_selected,
                defaults={'status': status}
            )
            Notification.objects.create( student=student, message=f"Your attendance for {enrollment.course.title} on {date_selected} has been marked as {status}.")
            messages.success(request, f"Attendance marked for {student.user.username}.")
            return redirect('students_enrolled', id=enrollment.course.id)

    return render(request, 'mark_attendance_single.html', {
        'student': student,
        'course': enrollment.course,
        'today': date.today()
    })


from django.db.models import Count, Q

@login_required
def view_attendance(request, course_id):
    if not hasattr(request.user, 'students_l'):
        return redirect('login')

    student = request.user.students_l
    course = get_object_or_404(Course, id=course_id)

    
    if not Enrollment.objects.filter(student=student, course=course).exists():
        messages.error(request, "You're not enrolled in this course.")
        return redirect('my_courses')

    
    records = Attendance.objects.filter(student=student, course=course).order_by('-date')

    total_days = records.count()
    present_days = records.filter(status__in=['P', 'L']).count()  # Present or Leave

    percentage = 0
    if total_days > 0:
        percentage = int((present_days / total_days) * 100)

    return render(request, 'student_attendance.html', {
        'course': course,
        'records': records,
        'percentage': percentage,
        'present_days': present_days,
        'total_days': total_days,
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, CourseMaterial, Instructor

@login_required
def upload_material(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Make sure only the assigned instructor can upload
    if not hasattr(request.user, 'instructor') or course.instructor != request.user.instructor:
        return redirect('unauthorized')  # or show error

    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        if title and file:
            CourseMaterial.objects.create(course=course, title=title, file=file)

            enrolled_student=Enrollment.objects.filter(course=course).select_related('student')
            for student in enrolled_student:
                Notification.objects.create(student=student.student,message=f"New material titled '{title}' was uploaded for the course '{course.title}'.")
           
            return redirect('instructor_dashboard')

    return render(request, 'upload_material.html', {'course': course})




@login_required
def view_material(request,c_id):
    course = get_object_or_404(Course, id=c_id)
    materials = CourseMaterial.objects.filter(course=course)
    return render(request, 'view_material.html', {'materials': materials, 'course': course})

@login_required
def notification(request):
    
    student = request.user.students_l
    notifications = Notification.objects.filter(student=student)
    return render(request, 'notifications.html', {'notifications': notifications})


from django.utils import timezone
from .models import Assignments, Notification, Enrollment

@login_required
def upload_assignment(request, c_id):
    course = get_object_or_404(Course, id=c_id)

    # Ensure only the assigned instructor can upload
    if not hasattr(request.user, 'instructor') or course.instructor != request.user.instructor:
        return redirect('unauthorized')

    if request.method == 'POST':
        title = request.POST['title']
        file = request.FILES.get('file')
        description = request.POST['description']
        deadline_str = request.POST['deadline']  # example: "2025-07-30T00:00"
        deadline = datetime.fromisoformat(deadline_str) # Should be in proper format: 'YYYY-MM-DDTHH:MM'

        if title and file and description and deadline:
            assignment = Assignments.objects.create(
                course=course,
                title=title,
                file=file,
                description=description,
                deadline=deadline
            )

            # Notify all enrolled students (move return outside loop)
            enrolled_students = Enrollment.objects.filter(course=course).select_related('student')
            for enrollment in enrolled_students:
                Notification.objects.create(
                    student=enrollment.student,
                    message=f"📘 New assignment: '{title}' in {course.title}. Deadline: {deadline}."
                )

            return redirect('instructor_dashboard')

    return render(request, 'upload_assignment.html', {'course': course})




@login_required
def view_assignment(request,c_id):
    course=get_object_or_404(Course,id=c_id)
    assignment=Assignments.objects.filter(course=course).order_by('-deadline')
    return render(request,'view_assignment.html',{'assignment':assignment,'course':course})




from django.utils import timezone

@login_required
def submit_assignment(request, c_id, a_id):
    course = get_object_or_404(Course, id=c_id)
    assignment = get_object_or_404(Assignments, id=a_id)
    student = request.user.students_l

    if request.method == 'POST':
        file = request.FILES.get('file')

        if not file:
            messages.error(request, "No file selected.")
            return redirect('view_assignment', c_id=c_id)

        is_late = timezone.now() > assignment.deadline

        Submissions.objects.create(
            student=student,
            assignment=assignment,
            file=file,
            is_late=is_late
        )

        messages.success(request, "Assignment submitted successfully." + (" (Late)" if is_late else ""))
        return redirect('my_courses')

    return render(request, 'submit_assignment.html', {
        'course': course,
        'assignment': assignment
    })

#1.Timetable and calendars
#2.marks
#3.Drop course


def home_pg(request):
    return render(request,'home_pg.html')



