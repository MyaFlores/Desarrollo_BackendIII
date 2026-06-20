import random
from django.core.management.base import BaseCommand
from students.models import Student, Course, Enrollment

class Command(BaseCommand):
    help = 'Carga datos de prueba con calificaciones altas'

    def handle(self, *args, **kwargs):
        students_data = [
            {'name': 'Ana García', 'email': 'ana.garcia@email.com'},
            {'name': 'Carlos López', 'email': 'carlos.lopez@email.com'},
            {'name': 'María Fernández', 'email': 'maria.fernandez@email.com'},
            {'name': 'José Martínez', 'email': 'jose.martinez@email.com'},
            {'name': 'Laura Rodríguez', 'email': 'laura.rodriguez@email.com'},
            {'name': 'Miguel Sánchez', 'email': 'miguel.sanchez@email.com'},
            {'name': 'Sofía Pérez', 'email': 'sofia.perez@email.com'},
            {'name': 'David González', 'email': 'david.gonzalez@email.com'},
            {'name': 'Elena Gómez', 'email': 'elena.gomez@email.com'},
            {'name': 'Javier Ruiz', 'email': 'javier.ruiz@email.com'},
        ]

        courses_data = [
            {'name': 'Matemáticas I', 'credits': 4, 'professor': 'Dr. Alejandro Torres'},
            {'name': 'Física I', 'credits': 4, 'professor': 'Dra. Patricia Ramírez'},
            {'name': 'Programación I', 'credits': 5, 'professor': 'Ing. Roberto Silva'},
            {'name': 'Química I', 'credits': 3, 'professor': 'Dra. Lucía Morales'},
            {'name': 'Inglés I', 'credits': 2, 'professor': 'Lic. María Elena Pérez'},
        ]

        print("🚀 Cargando datos de prueba con notas altas...")

        # Crear estudiantes
        students = []
        for data in students_data:
            student, created = Student.objects.get_or_create(
                email=data['email'],
                defaults={'name': data['name']}
            )
            students.append(student)

        # Crear cursos
        courses = []
        for data in courses_data:
            course, created = Course.objects.get_or_create(
                name=data['name'],
                defaults={'credits': data['credits'], 'professor': data['professor']}
            )
            courses.append(course)

        # Crear inscripciones con notas variadas
        # Algunos estudiantes tendrán notas altas (90-100)
        # Otros tendrán notas medias (70-89)
        # Para que el endpoint /top/ funcione correctamente
        
        # Definir notas para cada estudiante
        grades_distribution = []
        
        for i, student in enumerate(students):
            # Asignar notas altas a los primeros 3 estudiantes
            if i < 3:
                # Notas altas: 90-100
                grades = [random.randint(90, 100) for _ in range(random.randint(2, 4))]
                grades_distribution.append((student, grades, 'alta'))
            elif i < 6:
                # Notas medias-altas: 85-95
                grades = [random.randint(85, 95) for _ in range(random.randint(2, 4))]
                grades_distribution.append((student, grades, 'media-alta'))
            else:
                # Notas variadas: 60-100
                grades = [random.randint(60, 100) for _ in range(random.randint(1, 3))]
                grades_distribution.append((student, grades, 'variada'))
        
        # Crear inscripciones
        enrollment_count = 0
        for student, grades, _ in grades_distribution:
            selected_courses = random.sample(courses, min(len(grades), len(courses)))
            
            for i, course in enumerate(selected_courses):
                if i < len(grades):
                    grade = grades[i]
                    
                    try:
                        enrollment, created = Enrollment.objects.get_or_create(
                            student=student,
                            course=course,
                            defaults={'final_grade': grade}
                        )
                        if created:
                            enrollment_count += 1
                            print(f"✅ {student.name} → {course.name} (Nota: {grade})")
                        else:
                            enrollment.final_grade = grade
                            enrollment.save()
                            print(f"🔄 Actualizada: {student.name} → {course.name} (Nota: {grade})")
                    except:
                        pass

        # Verificar resultados
        print(f"\nResumen:")
        print(f"   - Estudiantes: {Student.objects.count()}")
        print(f"   - Cursos: {Course.objects.count()}")
        print(f"   - Inscripciones con nota: {Enrollment.objects.exclude(final_grade__isnull=True).count()}")
        
        # Mostrar estudiantes con promedio > 90
        print("\nEstudiantes con promedio > 90:")
        for student in Student.objects.all():
            enrollments = student.enrollments.exclude(final_grade__isnull=True)
            if enrollments.exists():
                avg = sum(e.final_grade for e in enrollments) / enrollments.count()
                if avg >= 90:
                    print(f"   - {student.name}: {avg:.2f}")