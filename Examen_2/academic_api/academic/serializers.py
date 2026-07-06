from rest_framework import serializers
from .models import Student, Course, Enrollment


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'enrollment_date']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'credits', 'professor']


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.name')
    course_name = serializers.ReadOnlyField(source='course.name')

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'course', 'course_name', 'final_grade']

    def validate_final_grade(self, value):
        if value is not None and (value < 0 or value > 10):
            raise serializers.ValidationError("La calificación debe estar entre 0 y 10")
        return value


class StudentCoursesSerializer(serializers.Serializer):
    course_name = serializers.CharField()
    professor = serializers.CharField()
    credits = serializers.IntegerField()
    final_grade = serializers.FloatField()