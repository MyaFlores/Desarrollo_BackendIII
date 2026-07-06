from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Student, Course, Enrollment
from .serializers import (
    StudentSerializer, CourseSerializer, EnrollmentSerializer, StudentCoursesSerializer)

# Estudiante
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# Cursos
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# Inscripciones 
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # No permitir que se inscriban dos veces en el mismo curso
        student = request.data.get('student')
        course = request.data.get('course')

        if student and course:
            exists = Enrollment.objects.filter(student=student, course=course).exists()
            if exists:
                return Response({
                    'error': 'El estudiante ya esta inscrito a este curso'
                }, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


# Endpoint personalizado (/api/students/<id>/courses/)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def student_courses(request, id):

   # Todos los cursos a los cuales el estudiante esta inscrito
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response({
            'error': 'Estudiante no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

    enrollments = student.enrollments.select_related('course')

    if not enrollments.exists():
        return Response({
            'message': 'El estudiante no esta inscrito en ningún curso',
            'student': student.name,
            'courses': []
        }, status=status.HTTP_200_OK)

    data = [
        {
            'course_name': e.course.name,
            'professor': e.course.professor,
            'credits': e.course.credits,
            'final_grade': e.final_grade
        }
        for e in enrollments
    ]

    return Response({
        'student': student.name,
        'total': len(data),
        'courses': data
    }, status=status.HTTP_200_OK)
        