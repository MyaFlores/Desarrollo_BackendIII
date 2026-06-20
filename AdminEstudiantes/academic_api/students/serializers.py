from rest_framework import serializers
from .models import Student, Course, Enrollment

# Serializer para Enrollment (anidado)
class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.name')
    course_name = serializers.ReadOnlyField(source='course.name')

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'course', 'course_name', 
                  'enrollment_date', 'final_grade']
        read_only_fields = ['enrollment_date']


# Serializer para Student
class StudentSerializer(serializers.ModelSerializer):
    # Campo calculado: promedio de calificaciones
    average_grade = serializers.SerializerMethodField()
    # Cantidad de cursos inscritos
    courses_count = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'enrollment_date', 'average_grade', 'courses_count']

    def get_average_grade(self, obj):
        """Calcula el promedio de calificaciones del estudiante"""
        enrollments = obj.enrollments.exclude(final_grade__isnull=True)
        if enrollments.exists():
            total = sum(e.final_grade for e in enrollments)
            return round(total / enrollments.count(), 2)
        return None

    def get_courses_count(self, obj):
        """Cuenta cuántos cursos tiene el estudiante"""
        return obj.enrollments.count()


# Serializer para Course
class CourseSerializer(serializers.ModelSerializer):
    # Cantidad de estudiantes inscritos
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'credits', 'professor', 'students_count']

    def get_students_count(self, obj):
        return obj.enrollments.count()


# Serializer para Student con sus cursos (detalle)
class StudentDetailSerializer(StudentSerializer):
    courses = serializers.SerializerMethodField()

    class Meta(StudentSerializer.Meta):
        fields = StudentSerializer.Meta.fields + ['courses']

    def get_courses(self, obj):
        enrollments = obj.enrollments.select_related('course')
        return [
            {
                'id': e.course.id,
                'name': e.course.name,
                'credits': e.course.credits,
                'professor': e.course.professor,
                'enrollment_date': e.enrollment_date,
                'final_grade': e.final_grade
            }
            for e in enrollments
        ]


# Serializer para Course con sus estudiantes (detalle)
class CourseDetailSerializer(CourseSerializer):
    students = serializers.SerializerMethodField()

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['students']

    def get_students(self, obj):
        enrollments = obj.enrollments.select_related('student')
        return [
            {
                'id': e.student.id,
                'name': e.student.name,
                'email': e.student.email,
                'enrollment_date': e.enrollment_date,
                'final_grade': e.final_grade
            }
            for e in enrollments
        ]