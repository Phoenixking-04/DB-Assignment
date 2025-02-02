from django.contrib import admin
from .models import Classroom, Department, Course, Instructor, Student, Enrollment, Teaching, Section

admin.site.register(Classroom)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Enrollment)
admin.site.register(Teaching)
admin.site.register(Section)
