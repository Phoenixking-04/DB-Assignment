from django.test import TestCase
from .models import Classroom, Department, Course, Instructor, Student, Enrollment, Teaching, Section

class ClassroomModelTest(TestCase):

    def test_classroom_creation(self):
        classroom = Classroom.objects.create(building="Science Block", room_number="101", capacity=50)
        self.assertEqual(classroom.building, "Science Block")
        self.assertEqual(classroom.room_number, "101")
        self.assertEqual(classroom.capacity, 50)

class DepartmentModelTest(TestCase):

    def test_department_creation(self):
        classroom = Classroom.objects.create(building="Admin Block", room_number="1A", capacity=30)
        department = Department.objects.create(department_name="Physics", building=classroom, budget=50000)
        self.assertEqual(department.department_name, "Physics")
        self.assertEqual(department.building, classroom)
        self.assertEqual(department.budget, 50000)

class CourseModelTest(TestCase):

    def test_course_creation(self):
        department = Department.objects.create(department_name="Chemistry")
        course = Course.objects.create(course_name="Organic Chemistry", department=department, credits=3)
        self.assertEqual(course.course_name, "Organic Chemistry")
        self.assertEqual(course.department, department)
        self.assertEqual(course.credits, 3)

class InstructorModelTest(TestCase):

    def test_instructor_creation(self):
        department = Department.objects.create(department_name="Biology")
        instructor = Instructor.objects.create(first_name="John", last_name="Doe", department=department, salary=75000)
        self.assertEqual(str(instructor), "John Doe")

class StudentModelTest(TestCase):

    def test_student_creation(self):
        department = Department.objects.create(department_name="Mathematics")
        student = Student.objects.create(first_name="Jane", last_name="Smith", total_credits=24, department=department)
        self.assertEqual(str(student), "Jane Smith")

class EnrollmentModelTest(TestCase):

    def test_enrollment_creation(self):
        department = Department.objects.create(department_name="Engineering")
        student = Student.objects.create(first_name="Mike", last_name="Jordan", total_credits=18, department=department)
        course = Course.objects.create(course_name="Electrical Engineering", department=department, credits=3)
        enrollment = Enrollment.objects.create(student=student, course=course, semester="Fall 2024")
        self.assertEqual(enrollment.student, student)
        self.assertEqual(enrollment.course, course)
        self.assertEqual(enrollment.semester, "Fall 2024")

class TeachingModelTest(TestCase):

    def test_teaching_creation(self):
        department = Department.objects.create(department_name="Arts")
        instructor = Instructor.objects.create(first_name="Alice", last_name="Wonder", department=department, salary=68000)
        course = Course.objects.create(course_name="Art History", department=department, credits=3)
        teaching = Teaching.objects.create(instructor=instructor, course=course)
        self.assertEqual(teaching.instructor, instructor)
        self.assertEqual(teaching.course, course)

class SectionModelTest(TestCase):

    def test_section_creation(self):
        department = Department.objects.create(department_name="Computer Science")
        course = Course.objects.create(course_name="Algorithms", department=department, credits=4)
        classroom = Classroom.objects.create(building="CS Block", room_number="202", capacity=40)
        section = Section.objects.create(course=course, section_id="A", semester="Spring 2025", year=2025, building=classroom, time_slot="10:00")
        self.assertEqual(section.course, course)
        self.assertEqual(section.section_id, "A")
        self.assertEqual(section.semester, "Spring 2025")
        self.assertEqual(section.year, 2025)
        self.assertEqual(section.building, classroom)
        self.assertEqual(section.time_slot, "10:00")
