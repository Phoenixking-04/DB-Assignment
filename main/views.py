from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from django.db.models import Avg
from .models import Course, Department, Enrollment, Student, Instructor, Teaching, Section, Classroom
from .forms import CourseForm, InstructorForm, StudentForm, EnrollmentForm, AssignInstructorForm, SectionForm, Enrollment  

def main_menu(request):
    return render(request, 'main/main_menu.html')

def view_courses(request):
    courses = Course.objects.all()
    return render(request, 'main/view_courses.html', {'courses': courses})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_students')
    else:
        form = StudentForm()
    return render(request, 'main/add_student.html', {'form': form})

def view_students(request):
    students = Student.objects.all()
    return render(request, 'main/view_students.html', {'students': students})

def course_detail(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    instructors = Instructor.objects.filter(teaching__course=course)
    enrollments = Enrollment.objects.filter(course=course)
    students = [enrollment.student for enrollment in enrollments]
    return render(request, 'main/course_detail.html', {'course': course, 'instructors': instructors, 'students': students})

def view_instructors(request):
    instructors = Instructor.objects.all()
    return render(request, 'main/view_instructors.html', {'instructors': instructors})

def search(request):
    return render(request, 'main/search.html')

def admin_menu(request):
    return render(request, 'main/admin_menu.html')

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            # Process start and end times to create a schedule string
            start_time = f"{request.POST['start_hour']}:{request.POST['start_minute']} {request.POST['start_period']}"
            end_time = f"{request.POST['end_hour']}:{request.POST['end_minute']} {request.POST['end_period']}"
            course.schedule = f"{start_time} - {end_time}"  # Example schedule format
            # Set room capacity from the form
            room_capacity = request.POST['room_capacity']
            course.room_capacity = room_capacity  # Ensuring room capacity is set
            course.save()
            return redirect('success_page')
    else:
        form = CourseForm()
    return render(request, 'main/add_course.html', {'form': form})

def add_instructor(request):
    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = InstructorForm()
    return render(request, 'main/add_instructor.html', {'form': form})

class StudentEnrollmentsView(View):
    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        enrollments = Enrollment.objects.filter(student=student)
        return render(request, 'main/student_enrollments.html', {'student': student, 'enrollments': enrollments})

def view_courses_with_department(request):
    courses = Course.objects.select_related('department').all()
    return render(request, 'main/view_courses_with_department.html', {'courses': courses})

def assign_advisor(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        instructor_id = request.POST.get('instructor_id')
        student = get_object_or_404(Student, pk=student_id)
        instructor = get_object_or_404(Instructor, pk=instructor_id)
        student.advisor = instructor  # Assign the instructor as the advisor
        student.save()
        return redirect('view_students')  # Redirect after assignment
    else:
        students = Student.objects.all()
        instructors = Instructor.objects.all()
    return render(request, 'main/assign_advisor.html', {'students': students, 'instructors': instructors})

def view_students_with_advisors(request):
    students = Student.objects.select_related('advisor').all()
    return render(request, 'main/view_students_with_advisors.html', {'students': students})

def average_salary_by_department(request):
    departments = Department.objects.annotate(avg_salary=Avg('instructor__salary'))
    return render(request, 'main/average_salary_by_department.html', {'departments': departments})

def find_instructors_by_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    instructors = Instructor.objects.filter(teaching__course=course)
    return render(request, 'main/find_instructors_by_course.html', {
        'course': course,
        'instructors': instructors,
    })


def all_courses_with_instructors(request):
    courses = Course.objects.prefetch_related('teaching_set__instructor').all()
    return render(request, 'main/all_courses_with_instructors.html', {'courses': courses})


def view_course_sections_with_room_capacity(request):
    courses = Course.objects.prefetch_related('section_set__building').all()
    return render(request, 'main/view_course_sections_with_room_capacity.html', {'courses': courses})

def find_students_by_minimum_credits(request, min_credits):
    students = Student.objects.filter(total_credits__gte=min_credits).order_by('total_credits')

    for student in students:
        print(f"{student.first_name} {student.last_name}: {student.total_credits} credits")

    return render(request, 'main/find_students_by_minimum_credits.html', {'students': students, 'min_credits': min_credits})


def enroll_student(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = EnrollmentForm()
    return render(request, 'main/enroll_student.html', {'form': form})


def assign_instructor_course(request):
    if request.method == 'POST':
        form = AssignInstructorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = AssignInstructorForm()
    return render(request, 'main/assign_instructor_course.html', {'form': form})

def success_page(request):
    return render(request, 'main/success_page.html')



def admin_view_courses(request):
    courses = Course.objects.all()
    return render(request, 'main/admin_view_courses.html', {'courses': courses})

def admin_delete_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    course.delete()
    return redirect('admin_view_courses')

def admin_view_students(request):
    students = Student.objects.all()
    return render(request, 'main/admin_view_students.html', {'students': students})

def admin_delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    student.delete()
    return redirect('admin_view_students')

def admin_view_instructors(request):
    instructors = Instructor.objects.all()
    return render(request, 'main/admin_view_instructors.html', {'instructors': instructors})

def admin_delete_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, instructor_id=instructor_id)
    instructor.delete()
    return redirect('admin_view_instructors')

def find_students_by_course(request, course_id):
    # Get the specific course or return a 404 if not found
    course = get_object_or_404(Course, course_id=course_id)

    # Fetch the enrolled students in the specified course
    enrollments = Enrollment.objects.filter(course=course)  # Fetch enrollments for that course
    students = [enrollment.student for enrollment in enrollments]  # Create a list of student objects

    # Render the course detail template
    return render(request, 'main/find_students_by_course.html', {
        'course': course,
        'students': students,
    })


def all_courses_with_students(request):
    # Fetch all courses and prefetch related enrollments and students for optimization
    courses = Course.objects.prefetch_related('enrollment_set__student').all()

    # Render the template with all courses and their enrolled students
    return render(request, 'main/all_courses_with_students.html', {'courses': courses})


def view_course_sections_with_room_capacity(request):
    courses = Course.objects.prefetch_related('sections__building').all()
    return render(request, 'main/view_course_sections_with_room_capacity.html', {'courses': courses})

