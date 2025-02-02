from django.urls import path
from .views import (
    main_menu, view_courses, view_students, add_student, view_instructors,
    course_detail, admin_menu, add_instructor, enroll_student, add_course,
    assign_instructor_course, search, view_courses_with_department,
    view_students_with_advisors, average_salary_by_department,
     find_instructors_by_course,
    assign_advisor,
    admin_view_courses, admin_delete_course,
    admin_view_students, admin_delete_student,
    admin_view_instructors, admin_delete_instructor,all_courses_with_students, all_courses_with_instructors,
    success_page, StudentEnrollmentsView, find_students_by_course, view_course_sections_with_room_capacity,find_students_by_minimum_credits
)

urlpatterns = [
    # Main menu and general views
    path('', main_menu, name='main_menu'),
    path('courses/', view_courses, name='view_courses'),
    path('students/', view_students, name='view_students'),
    path('add_student/', add_student, name='add_student'),
    path('instructors/', view_instructors, name='view_instructors'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('admin_menu/', admin_menu, name='admin_menu'),
    path('add_instructor/', add_instructor, name='add_instructor'),
    path('enroll_student/', enroll_student, name='enroll_student'),
    path('add_course/', add_course, name='add_course'),
    
    # Course student views
    path('courses/<int:course_id>/students/', find_students_by_course, name='find_students_by_course'),
    path('course_sections/', view_course_sections_with_room_capacity, name='view_course_sections_with_room_capacity'),
    path('courses/all/students/', all_courses_with_students, name='all_courses_with_students'),  # Renamed to clarify it's students
    path('courses/all/', all_courses_with_instructors, name='all_courses_with_instructors'),  # Keep this for all courses with instructors
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('courses/<int:course_id>/instructors/', find_instructors_by_course, name='find_instructors_by_course'),

    # Assignment and Observation
    path('assign_advisor/', assign_advisor, name='assign_advisor'),
    path('view_students_with_advisors/', view_students_with_advisors, name='view_students_with_advisors'),
    
    # Student enrollment views
    path('students/<int:student_id>/enrollments/', StudentEnrollmentsView.as_view(), name='student_enrollments'),

    # Admin views
    path('admin_view_courses/', admin_view_courses, name='admin_view_courses'),
    path('admin_delete_course/<int:course_id>/', admin_delete_course, name='admin_delete_course'),
    path('admin_view_students/', admin_view_students, name='admin_view_students'),
    path('admin_delete_student/<int:student_id>/', admin_delete_student, name='admin_delete_student'),
    path('admin_view_instructors/', admin_view_instructors, name='admin_view_instructors'),
    path('admin_delete_instructor/<int:instructor_id>/', admin_delete_instructor, name='admin_delete_instructor'),

    # Success page after actions
    path('success/', success_page, name='success_page'),

    # Search-related views
    path('search/', search, name='search'),  # Keeping this if you have a search functionality
    path('search/view_courses_with_department/', view_courses_with_department, name='view_courses_with_department'),
    path('search/average_salary_by_department/', average_salary_by_department, name='average_salary_by_department'),
    path('search/find_students_by_minimum_credits/<int:min_credits>/', find_students_by_minimum_credits, name='find_students_by_minimum_credits'),
    path('assign_instructor_course/', assign_instructor_course, name='assign_instructor_course'),
]