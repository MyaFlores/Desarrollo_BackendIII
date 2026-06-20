from django.urls import path
from . import views

urlpatterns = [
    # CRUD Estudiantes
    path('students/', views.StudentListCreateView.as_view(), name='student-list'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    
    # CRUD Cursos
    path('courses/', views.CourseListCreateView.as_view(), name='course-list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    
    # CRUD Inscripciones
    path('enrollments/', views.EnrollmentListCreateView.as_view(), name='enrollment-list'),
    path('enrollments/<int:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment-detail'),
    
    # Endpoints personalizados
    path('students/<int:student_id>/courses/', views.student_courses, name='student-courses'),
    path('courses/<int:course_id>/students/', views.course_students, name='course-students'),
    path('students/top/', views.top_students, name='top-students'),
    path('courses/popular/', views.popular_courses, name='popular-courses'),
    path('students/search/', views.search_students, name='search-students'),
]