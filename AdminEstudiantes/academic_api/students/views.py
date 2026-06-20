from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count, Avg, Q
from django.db import IntegrityError
from .models import Student, Course, Enrollment
from .serializers import (
    StudentSerializer, StudentDetailSerializer,
    CourseSerializer, CourseDetailSerializer,
    EnrollmentSerializer
)

# ==========================================
# CRUD: Estudiantes
# ==========================================

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_serializer_class(self):
        # Para el detalle usamos el serializer extendido
        if self.request.query_params.get('detail') == 'true':
            return StudentDetailSerializer
        return StudentSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer


# ==========================================
# CRUD: Cursos
# ==========================================

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.request.query_params.get('detail') == 'true':
            return CourseDetailSerializer
        return CourseSerializer


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


# ==========================================
# CRUD: Inscripciones
# ==========================================

class EnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            self.perform_create(serializer)
            return Response({
                'success': True,
                'message': 'Inscripción creada exitosamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({
                'success': False,
                'message': 'El estudiante ya está inscrito en este curso'
            }, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


# ==========================================
# ENDPOINTS PERSONALIZADOS
# ==========================================

# 1. Obtener todos los cursos de un estudiante
@api_view(['GET'])
def student_courses(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Estudiante no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    enrollments = student.enrollments.select_related('course')
    data = [
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
    
    return Response({
        'success': True,
        'student': student.name,
        'total': len(data),
        'courses': data
    })


# 2. Obtener todos los estudiantes inscritos en un curso
@api_view(['GET'])
def course_students(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Curso no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    enrollments = course.enrollments.select_related('student')
    data = [
        {
            'id': e.student.id,
            'name': e.student.name,
            'email': e.student.email,
            'enrollment_date': e.enrollment_date,
            'final_grade': e.final_grade
        }
        for e in enrollments
    ]
    
    return Response({
        'success': True,
        'course': course.name,
        'total': len(data),
        'students': data
    })


# 3. Obtener estudiantes con promedio mayor a 90
@api_view(['GET'])
def top_students(request):
    # Obtener todos los estudiantes y calcular su promedio
    students = Student.objects.all()
    top_students = []
    
    for student in students:
        enrollments = student.enrollments.exclude(final_grade__isnull=True)
        if enrollments.exists():
            avg = sum(e.final_grade for e in enrollments) / enrollments.count()
            if avg >= 90:
                top_students.append({
                    'id': student.id,
                    'name': student.name,
                    'email': student.email,
                    'average_grade': round(avg, 2),
                    'courses_taken': enrollments.count()
                })
    
    # Ordenar por promedio descendente
    top_students.sort(key=lambda x: x['average_grade'], reverse=True)
    
    return Response({
        'success': True,
        'total': len(top_students),
        'students': top_students
    })


# 4. Obtener cursos con más de 5 estudiantes inscritos
@api_view(['GET'])
def popular_courses(request):
    # Usar annotate y filter para consulta eficiente
    popular = Course.objects.annotate(
        students_count=Count('enrollments')
    ).filter(students_count__gt=5).order_by('-students_count')
    
    data = [
        {
            'id': course.id,
            'name': course.name,
            'professor': course.professor,
            'credits': course.credits,
            'students_count': course.students_count
        }
        for course in popular
    ]
    
    return Response({
        'success': True,
        'total': len(data),
        'courses': data
    })


# 5. Buscar estudiantes por nombre (query parameter)
@api_view(['GET'])
def search_students(request):
    query = request.query_params.get('q', '')
    
    if not query:
        return Response({
            'success': False,
            'message': 'Debes proporcionar un término de búsqueda (?q=nombre)'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Búsqueda insensible a mayúsculas
    students = Student.objects.filter(name__icontains=query)
    serializer = StudentSerializer(students, many=True)
    
    return Response({
        'success': True,
        'query': query,
        'total': students.count(),
        'results': serializer.data
    })