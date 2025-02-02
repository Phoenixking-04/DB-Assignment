from django import forms
from .models import Course, Instructor, Student, Enrollment, Teaching, Section
from datetime import datetime
from django.core.exceptions import ValidationError


class CourseForm(forms.ModelForm):
    course_id = forms.IntegerField(required=True)
    start_hour = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1, 13)])
    start_period = forms.ChoiceField(choices=[('AM', 'AM'), ('PM', 'PM')])
    end_hour = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(1, 13)])
    end_period = forms.ChoiceField(choices=[('AM', 'AM'), ('PM', 'PM')])

    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'department', 'credits', 'start_hour', 'start_period', 'end_hour', 'end_period']

    def clean_course_id(self):
        course_id = self.cleaned_data.get('course_id')
        if Course.objects.filter(course_id=course_id).exists():
            raise forms.ValidationError("Course with this ID already exists.")
        return course_id

    def clean_credits(self):
        credits = self.cleaned_data.get('credits')
        if not (1 <= credits <= 3):
            raise forms.ValidationError("Credits must be between 1 and 3.")
        return credits

    def clean_schedule(self):
        start_hour = self.cleaned_data.get('start_hour')
        start_period = self.cleaned_data.get('start_period')
        end_hour = self.cleaned_data.get('end_hour')
        end_period = self.cleaned_data.get('end_period')

        start_time = f"{start_hour} {start_period}"
        end_time = f"{end_hour} {end_period}"

        start_time = datetime.strptime(start_time, '%I %p')
        end_time = datetime.strptime(end_time, '%I %p')

        if start_time >= end_time:
            raise forms.ValidationError("End time must be later than start time.")
        schedule = f"Schedule: {start_hour} {start_period} to {end_hour} {end_period}"
        return schedule

    def save(self, commit=True):
        course = super().save(commit=False)
        course.schedule = self.clean_schedule()
        if commit:
            course.save()
        return course



class InstructorForm(forms.ModelForm):
    instructor_id = forms.IntegerField(required=True)

    class Meta:
        model = Instructor
        fields = ['instructor_id', 'first_name', 'last_name', 'department', 'salary']

    def clean_instructor_id(self):
        instructor_id = self.cleaned_data.get('instructor_id')
        if Instructor.objects.filter(instructor_id=instructor_id).exists():
            raise forms.ValidationError("Instructor with this ID already exists.")
        return instructor_id





def validate_student_id(value):
    if len(str(value)) != 5:
        raise ValidationError("Student ID must be exactly 5 digits.")

class StudentForm(forms.ModelForm):
    student_id = forms.IntegerField(validators=[validate_student_id], required=True)

    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'total_credits', 'date_of_birth', 'advisor', 'department']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'advisor': forms.Select(attrs={'class': 'advisor-select'}),
            'department': forms.Select(attrs={'class': 'department-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['advisor'].queryset = Instructor.objects.all()
        
    
    

class EnrollmentForm(forms.ModelForm):
    grade = forms.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], required=True)

    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'semester', 'grade']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['semester'].choices = self.get_unique_semesters()

    def get_unique_semesters(self):
        semesters = Enrollment.objects.values_list('semester', flat=True).distinct().order_by('semester')
        return [(semester, semester) for semester in semesters]

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get("student")
        course = cleaned_data.get("course")
        semester = cleaned_data.get("semester")

        if Enrollment.objects.filter(student=student, semester=semester, course=course).exists():
            raise forms.ValidationError(f"Student {student} is already enrolled in the course {course} for semester {semester}.")

        return cleaned_data

    def save(self, commit=True):
        enrollment = super().save(commit=False)

        if commit:
            enrollment.save()
            # Update total credits for the student
            student = enrollment.student
            student.total_credits += enrollment.course.credits
            student.save()

        return enrollment




class AssignInstructorForm(forms.ModelForm):
    class Meta:
        model = Teaching
        fields = ['instructor', 'course']

    def clean(self):
        cleaned_data = super().clean()
        instructor = cleaned_data.get('instructor')
        course = cleaned_data.get('course')

        if Teaching.objects.filter(instructor=instructor, course=course).exists():
            raise forms.ValidationError(f"Instructor {instructor} is already assigned to course {course}.")

        return cleaned_data




class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['course', 'section_id', 'semester', 'year', 'building', 'time_slot']
