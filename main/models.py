from django.db import models

class Classroom(models.Model):
    building = models.CharField(max_length=100)
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.building} - Room {self.room_number}"

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    building = models.ForeignKey(Classroom, on_delete=models.CASCADE)  # Assuming a department belongs to one building
    budget = models.IntegerField()

    def __str__(self):
        return self.department_name

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    credits = models.IntegerField()
    schedule = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.course_name


class Instructor(models.Model):
    instructor_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    salary = models.FloatField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    total_credits = models.IntegerField()
    date_of_birth = models.DateField(null=True, blank=True)
    advisor = models.ForeignKey('Instructor', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    grade = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course', 'semester')
        
        

class Teaching(models.Model):
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

class Section(models.Model):
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE)
    section_id = models.CharField(max_length=10)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    building = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    time_slot = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.course.course_name} - Section {self.section_id} ({self.semester} {self.year})"
