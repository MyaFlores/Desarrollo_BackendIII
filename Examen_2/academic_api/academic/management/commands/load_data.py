import random
from django.core.management.base import BaseCommand
from academic.models import Student, Course, Enrollment

class Command(BaseCommand):
    help = 'Carga datos de prueba (3 estudiantes, 3 cursos, 5 inscripciones)'

    def handle(self, *args, **kwargs):
        print("Cargando datos de prueba...")

        # 3 Estudiantes
        students_data = [
            {'name': 'Ana García', 'email': 'ana@email.com'},
            {'name': 'Carlos López', 'email': 'carlos@email.com'},
            {'name': 'María Fernández', 'email': 'maria@email.com'},
            {'name': 'Abigail Reyes', 'email': 'abby@email.com'},

        ]

        students = []
        for data in students_data:
            student, created = Student.objects.get_or_create(
                email=data['email'],
                defaults={'name': data['name']}
            )
            students.append(student)
            if created:
                print(f"Estudiante creado: {student.name}")

        # 3 Cursos
        courses_data = [
            {'name': 'Matemáticas I', 'credits': 4, 'professor': 'Dr. Alejandro Torres'},
            {'name': 'Física I', 'credits': 4, 'professor': 'Dra. Patricia Ramírez'},
            {'name': 'Programación I', 'credits': 5, 'professor': 'Ing. Roberto Silva'},
        ]

        courses = []
        for data in courses_data:
            course, created = Course.objects.get_or_create(
                name=data['name'],
                defaults={'credits': data['credits'], 'professor': data['professor']}
            )
            courses.append(course)
            if created:
                print(f"Curso creado: {course.name}")

        # 5 Inscripciones
        enrollments_data = [
            {'student': students[0], 'course': courses[0], 'final_grade': 9.5},
            {'student': students[0], 'course': courses[1], 'final_grade': 8.0},
            {'student': students[1], 'course': courses[0], 'final_grade': 7.5},
            {'student': students[1], 'course': courses[2], 'final_grade': 9.0},
            {'student': students[2], 'course': courses[1], 'final_grade': 8.5},
        ]

        for data in enrollments_data:
            enrollment, created = Enrollment.objects.get_or_create(
                student=data['student'],
                course=data['course'],
                defaults={'final_grade': data['final_grade']}
            )
            if created:
                print(f"Inscripción: {data['student'].name} → {data['course'].name} (Nota: {data['final_grade']})")

        print(f"\nResumen:")
        print(f"   - Estudiantes: {Student.objects.count()}")
        print(f"   - Cursos: {Course.objects.count()}")
        print(f"   - Inscripciones: {Enrollment.objects.count()}")