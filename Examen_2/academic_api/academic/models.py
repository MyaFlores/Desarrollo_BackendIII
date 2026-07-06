from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta: 
        ordering = ['name']

class Course(models.Model):
    name = models.CharField(max_length=100)
    credits = models.IntegerField(validators=[MinValueValidator(1)])
    professor = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    final_grade = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], 
        null=True, 
        blank=True
    )

    class Meta: 
        #El sistema no va a permitir que un estudiante este registrado en el mismo curso dos veces
        unique_together = ('student', 'course')
        ordering = ['student']

    def __str__(self):
        return f"{self.student.name} -> {self.course.name} ({self.final_grade})"