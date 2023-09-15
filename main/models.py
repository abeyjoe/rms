from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=50)
    core_units = models.SmallIntegerField()
    elective_units = models.SmallIntegerField()
    general_units = models.SmallIntegerField()

    @property
    def total_units(self):
        return self.core_units + self.elective_units + self.general_units

    def __str__(self):
        return self.name + " : " + str(self.total_units)
    
SEMESTER_CHOICES = (
    ("1st Semester", "1st Semester"),
    ("2nd Semester", "2nd Semester"),
)

LEVEL_CHOICES = (
    ("ND1", "ND1"),
    ("ND2", "ND2"),
    ("HND1", "HND1"),
    ("HND2", "HND2"),
)
 
PROGRAM_CHOICES = (
    ("ND", "ND"),
    ("HND", "HND"),
)

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    unit = models.DecimalField(max_digits=5, decimal_places=2)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    course_type = models.CharField(max_length=10)
    semester = models.CharField(max_length=20,choices=SEMESTER_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.code}: {self.name}"
class Student(models.Model):
    name = models.CharField(max_length=100)
    matric_no = models.CharField(max_length=100, unique=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    program = models.CharField(max_length=15, choices=PROGRAM_CHOICES)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " : " + self.department

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.SmallIntegerField()
    def __str__(self):
        return self.student + " : " + self.course + " : " + self.score
