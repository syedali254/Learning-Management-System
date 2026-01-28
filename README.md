

# 📚 Django LMS (Learning Management System)

A full-featured **Learning Management System (LMS)** built with **Django**, designed for **students and instructors** with a clean **UI/UX** and modern functionality.
This project allows instructors to manage courses, assignments, and attendance, while students can enroll in courses, track attendance, submit assignments, and view notifications.

---

## 🔹 Features

### **User Authentication**

* Secure **login and logout** system for students and instructors.
* Role-based dashboards:

  * **Instructor Dashboard**: Manage courses, students, assignments, and attendance.
  * **Student Dashboard**: Enroll in courses, view assignments, and track progress.

### **Course Management**

* Instructors can **add, update, and view courses**.
* Students can **browse and enroll** in courses.
* View students enrolled in each course.

### **Attendance System**

* Instructors can **mark attendance** for students (Present, Absent, Leave).
* Automatic notifications sent to students when attendance is updated.
* Students can **view their attendance records and percentages**.

### **Course Materials**

* Instructors can **upload course materials** (PDFs, docs, or other files).
* Students can **view/download course materials**.
* Notifications sent automatically for new uploads.

### **Assignments & Submissions**

* Instructors can **create assignments** with deadlines and descriptions.
* Students can **submit assignments** with automatic late detection.
* Notifications for all enrolled students on new assignments.

### **Notifications**

* Students receive notifications for:

  * Attendance updates
  * New materials
  * New assignments
* Clean UI for easy access and tracking.

### **Additional Features**

* Clean, responsive **UI/UX** with clear separation of dashboards.
* Planned features (future enhancements):

  1. **Timetable & calendars** for courses.
  2. **Marks/grades management**.
  3. **Drop course functionality** for students.

---

## 🔹 Tech Stack

* **Backend**: Django 4.x
* **Database**: SQLite (default) / PostgreSQL (optional)
* **Frontend**: HTML, CSS, Bootstrap (or any modern CSS framework for clean UI)
* **Python Version**: 3.10+

---

## 🔹 Installation

1. **Clone the repository**



2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

* Windows:

```bash
venv\Scripts\activate
```

* Linux/Mac:

```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Apply migrations**

```bash
python manage.py migrate
```

6. **Create a superuser**

```bash
python manage.py createsuperuser
```

7. **Run the development server**

```bash
python manage.py runserver
```

8. **Access the project**

* Open your browser at `http://127.0.0.1:8000/`

---

## 🔹 Project Structure

```

├─ students/                  # Main Django app
│  ├─ templates/             # HTML templates for UI
│  ├─ static/                # CSS, JS, and images
│  ├─ models.py              # All models: User, Course, Attendance, Assignments, Submissions, Notifications
│  ├─ views.py               # All views and functionalities
│  ├─ urls.py                # App-specific URLs
├─ django_lms/               # Project settings
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
├─ manage.py                 # Django management file
```

---

## 🔹 UI Overview

* **Login Page**: Simple, clean login interface for students and instructors.
* **Instructor Dashboard**: Manage courses, upload materials, mark attendance, and create assignments.
* **Student Dashboard**: View available courses, enroll, track attendance, and submit assignments.
* **Notifications**: Real-time updates for all student activities.
* **Course Materials**: Organized, easy-to-access course files.

> The project focuses on **clean UI/UX**, with intuitive navigation and clear role-based access.

---

## 🔹 Key Models

* **User**: Extended for students (`students_l`) and instructors (`instructor`) roles.
* **Course**: Courses created by instructors.
* **Enrollment**: Students enrolled in courses.
* **Attendance**: Daily attendance records for students.
* **Notification**: Messages sent to students for attendance, materials, and assignments.
* **Assignments**: Course-specific assignments uploaded by instructors.
* **Submissions**: Student submissions with late detection.

---

## 🔹 Future Enhancements

* Add **grading system / marks tracking**.
* Implement **timetable and calendar integration**.
* Allow students to **drop courses**.
* Email or push **real-time notifications**.
* Improve **UI/UX** with modern front-end frameworks (React / TailwindCSS).
* Use Ai for Adding advanced features.

---

## 🔹 Author

**Muhammad Ali**

* Portfolio: [LinkedIn](https://www.linkedin.com/in/muhammad-ali-07185431a)
* Skills: Django, Python, HTML/CSS, Bootstrap, Full-Stack Development

---

