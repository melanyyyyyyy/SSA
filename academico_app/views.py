import json

from django.http import JsonResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.messages import get_messages
from django.db import models
from django.db.models import Q, Avg, Count

from .models import Student, Subject, User, Comment, UserRole, GradeRecord, AttendanceRecord
from .decorators import professor_required, student_required


def home(request:HttpRequest):
    return render(request, 'home.html')


# Vista para el login
def login_view(request : HttpRequest):
    user : User = request.user
    if user.is_authenticated:
        match user.get_role():
            case UserRole.PROFESSOR:
                return redirect('/professor/dashboard/')
            case UserRole.STUDENT:
                return redirect('/student/dashboard/')
            case UserRole.ADMIN:
                return redirect('/admin/')
    return render(request, 'auth/login.html')


@require_POST
def login_check(request: HttpRequest):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            is_professor = user.is_professor()
            is_student = user.is_student()
            is_staff = user.is_staff
            
            if not any([is_professor, is_student, is_staff]):
                logout(request) 
                return JsonResponse({
                    'success': False,
                    'error': 'El usuario no tiene un rol válido asignado'
                }, status=403)

            return JsonResponse({
                'success': True,
                'redirect_url': (
                    '/professor/dashboard/' if is_professor else
                    '/student/dashboard/' if is_student else
                    '/admin/'
                )
            })
        else:
            return JsonResponse({'success': False, 'error': 'Credenciales inválidas'}, status=401)
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)



# Vista para el logout
@login_required
def logout_view(request: HttpRequest):
    logout(request)
    return redirect('login')



# Vista para cargar el dashboard del profesor (es la vista que aparece después del login para el profesor)
@login_required
@professor_required
def professor_dashboard(request: HttpRequest):
    professor = request.user.professor
    
    subjects = (
            Subject.objects.filter(professor=professor, completed=False)
            .order_by("year") 
            .distinct() 
        )
    
    comments = Comment.objects.filter(
        professor=professor
    ).order_by('-date')

    context = {
        "subjects": subjects,
        "comments": comments,
    }
        
    return render(request, 
        'professor/professor_dashboard.html', 
        context)
    


# Vista que se carga al seleccionar una asignatura desde el dashboard del profesor 
@login_required
@professor_required
def subject_view(request: HttpRequest, subject_id: int):
    professor = request.user.professor
    subject = get_object_or_404(Subject, id=subject_id, professor=professor)
    
    students = Student.objects.filter(
        career=subject.career,
        academic_year=subject.year
    )
    
    student_data = []
    for student in students:
        grades = GradeRecord.objects.filter(student=student, subject=subject)
        attendances = AttendanceRecord.objects.filter(student=student, subject=subject)
        
        grade_avg = grades.aggregate(avg=models.Avg('grade'))['avg']
        if grade_avg is not None:
            grade_avg = round(float(grade_avg), 1)
        else:
            grade_avg = "N/A" 
        
        total_attendance = attendances.count()
        if total_attendance > 0:
            attended_count = attendances.filter(attended=True).count()
            attendance_percent = round((attended_count / total_attendance) * 100, 1)
            attendance_display = f"{attendance_percent}%"
        else:
            attendance_display = "N/A"
        
        student_data.append({
            'student': student,
            'grade_avg': grade_avg,
            'attendance': attendance_display,
            'has_grades': grades.exists(), 
            'has_attendance': attendances.exists() 
        })
    
    context = {
        'subject': subject,
        'student_data': student_data,
        'is_completed': subject.completed
    }
    
    return render(request, 'professor/subject_view.html', context)



# Vista para el botón de agregar registro de asistencia para todo el grupo de estudiantes 
@login_required
@professor_required
def register_attendance(request: HttpRequest, subject_id: int):
    professor = request.user.professor
    subject = get_object_or_404(Subject, id=subject_id, professor=professor)
    
    students = Student.objects.filter(
        career=subject.career,
        academic_year=subject.year
    )
    
    context = {
        'students': students,
        'subject': subject,
    }
    
    if request.method == 'POST':
        session_date = request.POST.get('session_date')
        if not session_date:
            messages.error(request, "Debes seleccionar una fecha.")
            storage = get_messages(request)
            message_list = [{"text": m.message, "tag": m.tags} for m in storage]
            return JsonResponse({
                "success": False,
                "messages": message_list
            }, status=400)
        
        for student in students:
            attended = f'attendance_{student.id}' in request.POST
            AttendanceRecord.objects.create(
                student=student,
                subject=subject,
                attended=attended,
                date=session_date
            )
        messages.success(request, "Asistencia registrada correctamente.")
        return JsonResponse({
            "success": True,
            "redirect_url": f"/professor/dashboard/{subject_id}"
        })
        
    return render(request, 'professor/register_attendance.html', context)


# Vista para el botón de agregar registro de evaluación para todo el grupo de estudiantes 
@login_required
@professor_required
def register_grade(request: HttpRequest, subject_id: int):
    professor = request.user.professor
    subject = get_object_or_404(Subject, id=subject_id, professor=professor)

    students = Student.objects.filter(
        career=subject.career,
        academic_year=subject.year
    )

    context = {
        'students': students,
        'subject': subject,
    }

    if request.method == 'POST':
        grade_name = request.POST.get('grade_name', '').strip()
        session_date = request.POST.get('session_date')
        if not grade_name:
            messages.error(request, "Debes ingresar el nombre de la evaluación.")
        if not session_date:
            messages.error(request, "Debes seleccionar una fecha.")
        if not grade_name or not session_date:
            storage = get_messages(request)
            message_list = [{"text": m.message, "tag": m.tags} for m in storage]
            return JsonResponse({
                "success": False,
                "messages": message_list
            }, status=400)

        for student in students:
            grade_value = request.POST.get(f'grade_{student.id}', '').strip()
            if grade_value:
                try:
                    grade_value = float(grade_value)
                    if 2 <= grade_value <= 5:
                        GradeRecord.objects.create(
                            student=student,
                            subject=subject,
                            grade=grade_value,
                            date=session_date,
                            name=grade_name
                        )
                    else:
                        messages.error(request, f"La nota para {student.user.get_full_name()} debe estar entre 2 y 5.")
                except ValueError:
                    messages.error(request, f"Nota inválida para {student.user.get_full_name()}.")
            else:
                messages.error(request, f"Debes ingresar una nota para {student.user.get_full_name()}.")

        storage = get_messages(request)
        message_list = [{"text": m.message, "tag": m.tags} for m in storage]

        if any(m['tag'] == 'error' for m in message_list):
            return JsonResponse({
                "success": False,
                "messages": message_list
            }, status=400)

        messages.success(request, "Evaluación registrada correctamente.")
        return JsonResponse({
            "success": True,
            "redirect_url": f"/professor/dashboard/{subject_id}"
        })

    return render(request, 'professor/register_grade.html', context)



# Vista para agregar un comentario
@login_required
@professor_required
def comment_add(request: HttpRequest, username: str, subject_id: int):
    student_user = get_object_or_404(User, username=username)
    student = student_user.student
    professor = request.user.professor
    subject = get_object_or_404(Subject, pk=subject_id, professor=professor, career=student.career)

    if request.method == 'POST':
        comment_text = request.POST.get('comment', '').strip()

        if not comment_text:
            messages.error(request, "El comentario no puede estar vacío")
            return redirect('comment_add', username=username, subject_id=subject_id)

        try:
            Comment.objects.create(
                student=student,
                professor=professor,
                subject=subject,
                comment=comment_text
            )
            messages.success(request, "Comentario guardado exitosamente")
            return redirect('subject_view', subject_id=subject_id)
        except Exception as e:
            messages.error(request, f"Error al guardar el comentario: {str(e)}")
            return redirect('comment_add', username=username, subject_id=subject_id)

    context = {
        'subject': subject,
        'student_name': student_user.get_full_name(),
        'student_username': student_user.username,
    }
    return render(request, 'professor/comment_add.html', context)



# Vista para eliminar un comentario
@login_required
@professor_required
@require_POST
def delete_comment(request: HttpRequest, comment_id: int):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        messages.error(request, "Comentario no encontrado")
        storage = get_messages(request)
        message_list = [{"text": m.message, "tag": m.tags} for m in storage]
        return JsonResponse({"success": False, "messages": message_list}, status=404)
    
    try:
        comment.delete()
        messages.success(request, "Cambios guardados exitosamente")
    except Exception as e:
        messages.error(request, f"Error al eliminar el comentario: {str(e)}")
        storage = get_messages(request)
        message_list = [{"text": m.message, "tag": m.tags} for m in storage]
        return JsonResponse({"success": False, "messages": message_list}, status=500)
    
    storage = get_messages(request)
    message_list = [{"text": m.message, "tag": m.tags} for m in storage]
    return JsonResponse({"success": True, "messages": message_list})



# Vista para editar un comentario 
@login_required
@professor_required
def edit_comment(request: HttpRequest, comment_id: int ):
    comment = get_object_or_404(Comment, id=comment_id)
    username = comment.student.user.username
    student_user = get_object_or_404(User, username=username)
    student = student_user.student  
    professor = request.user.professor

    subjects = Subject.objects.filter(
        professor=professor,
        career=student.career
    ).filter(
        Q(subject_register__student=student) | Q(subject_attendance__student=student)
    ).distinct()
    
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        comment.comment = request.POST.get('comment')
        comment.subject = get_object_or_404(Subject, id=subject_id)
        comment.save()
        messages.success(request, "Cambios guardados exitosamente")
        return redirect('professor_dashboard')

    context = {
        'subjects': subjects,
        'student_name': student_user.get_full_name(),
        'student_username': username,
        'edit_comment': True,
        'comment': comment.comment,
        'subject_selected': comment.subject.id,
        'subject_name': comment.subject.name,
        'subject_year': comment.subject.year,
    }

    return render(request, 'professor/comment_add.html', context)

def cancel_comment(request, username):
    messages.error(request, "El usuario canceló la acción.")
    return redirect('professor_dashboard')



# Vista para cargar el historial de registros 
@login_required
@professor_required
def history(request: HttpRequest, subject_id: int):
    professor = request.user.professor
    subject = get_object_or_404(Subject, id=subject_id, professor=professor)

    attendance_history = (
        AttendanceRecord.objects
        .filter(subject=subject)
        .values('date')
        .annotate(
            avg_attendance=Avg('attended'),
            total=Count('id')
        )
        .order_by('-date')
    )
    
    attendance_history = [
        {
            **record,
            'avg_attendance': round(record['avg_attendance'] * 100, 2) if record['avg_attendance'] is not None else None
        }
        for record in attendance_history
    ]

    grade_history = (
        GradeRecord.objects
        .filter(subject=subject)
        .values('date', 'name')
        .annotate(
            avg_grade=Avg('grade'),
            total=Count('id')
        )
        .order_by('-date', 'name')
    )

    grade_history = [
        {
            **record,
            'avg_grade': round(record['avg_grade'], 2) if record['avg_grade'] is not None else None
        }
        for record in grade_history
    ]

    context = {
        'subject': subject,
        'attendance_history': attendance_history,
        'grade_history': grade_history,
    }
    return render(request, 'professor/history/history.html', context)



# Vista para eliminar un registro de asistencia para todo el grupo de estudiantes
@login_required
@professor_required
@require_POST
def delete_attendance_record(request):
    subject_id = request.POST.get('subject_id')
    date = request.POST.get('date')
    try:
        subject = get_object_or_404(Subject, id=subject_id, professor=request.user.professor)
        deleted, _ = AttendanceRecord.objects.filter(subject=subject, date=date).delete()
        if deleted:
            return JsonResponse({"success": True, "messages": [{"text": "Registro de asistencia eliminado.", "tag": "success"}]})
        else:
            return JsonResponse({"success": False, "messages": [{"text": "No se encontró el registro.", "tag": "error"}]}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "messages": [{"text": f"Error: {str(e)}", "tag": "error"}]}, status=500)



# Vista para eliminar un registro de evaluación para todo el grupo de estudiantes
@login_required
@professor_required
@require_POST
def delete_grade_record(request):
    subject_id = request.POST.get('subject_id')
    date = request.POST.get('date')
    name = request.POST.get('name')
    try:
        subject = get_object_or_404(Subject, id=subject_id, professor=request.user.professor)
        deleted, _ = GradeRecord.objects.filter(subject=subject, date=date, name=name).delete()
        if deleted:
            return JsonResponse({"success": True, "messages": [{"text": "Registro de evaluación eliminado.", "tag": "success"}]})
        else:
            return JsonResponse({"success": False, "messages": [{"text": "No se encontró el registro.", "tag": "error"}]}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "messages": [{"text": f"Error: {str(e)}", "tag": "error"}]}, status=500)
    
    

# Vista para cargar los detalles del registro de asistencia
@login_required
@professor_required
def history_detail_attendance(request, subject_id, date):
    professor = request.user.professor
    subject = get_object_or_404(Subject, id=subject_id, professor=professor)
    records = AttendanceRecord.objects.filter(subject=subject, date=date).select_related('student__user')

    if request.method == 'POST':
        error = False
        for record in records:
            attended = f'attendance_{record.id}' in request.POST
            record.attended = attended
            record.save()
        messages.success(request, "Cambios guardados exitosamente.")
        storage = get_messages(request)
        message_list = [{"text": m.message, "tag": m.tags} for m in storage]
        return JsonResponse({"success": not error, "messages": message_list})

    context = {
        'subject': subject,
        'date': date,
        'records': records,
    }
    return render(request, 'professor/history/history_detail_attendance.html', context)



# Vista para cargar los detalles del registro de de evaluación
@login_required
@professor_required
def history_detail_grade(request, subject_id, date, name):
    professor = request.user.professor
    subject = get_object_or_404(Subject, id=subject_id, professor=professor)
    records = GradeRecord.objects.filter(subject=subject, date=date, name=name).select_related('student__user')

    if request.method == 'POST':
        error = False
        for record in records:
            grade_value = request.POST.get(f'grade_{record.id}', '').strip()
            if grade_value:
                try:
                    grade_value = float(grade_value)
                    if 2 <= grade_value <= 5:
                        record.grade = grade_value
                        record.save()
                    else:
                        messages.error(request, f"La nota para {record.student.user.get_full_name()} debe estar entre 2 y 5.")
                        error = True
                except ValueError:
                    messages.error(request, f"Nota inválida para {record.student.user.get_full_name()}.")
                    error = True
            else:
                messages.error(request, f"Debes ingresar una nota para {record.student.user.get_full_name()}.")
                error = True

        storage = get_messages(request)
        message_list = [{"text": m.message, "tag": m.tags} for m in storage]

        if error:
            return JsonResponse({"success": False, "messages": message_list}, status=400)
        messages.success(request, "Cambios guardados exitosamente.")
        return JsonResponse({"success": True, "messages": message_list})

    context = {
        'subject': subject,
        'date': date,
        'name': name,
        'records': records,
    }
    return render(request, 'professor/history/history_detail_grade.html', context)



# Vista para cargar los detalles de asistencia y evaluación de un estudiante
@login_required
@professor_required
def student_subject_detail(request, subject_id, student_id):
    professor = request.user.professor
    subject = get_object_or_404(Subject, id=subject_id, professor=professor)
    student = get_object_or_404(Student, id=student_id)

    attendance_records = AttendanceRecord.objects.filter(subject=subject, student=student).order_by('-date')
    grade_records = GradeRecord.objects.filter(subject=subject, student=student).order_by('-date', 'name')

    if request.method == 'POST':
        edit_type = request.GET.get('edit')
        error = False
        if edit_type == 'attendance':
            for record in attendance_records:
                attended = f'attendance_{record.id}' in request.POST
                record.attended = attended
                record.save()
            messages.success(request, "Cambios de asistencia guardados exitosamente.")
        elif edit_type == 'grade':
            for record in grade_records:
                grade_value = request.POST.get(f'grade_{record.id}', '').strip()
                if grade_value:
                    try:
                        grade_value = float(grade_value)
                        if 2 <= grade_value <= 5:
                            record.grade = grade_value
                            record.save()
                        else:
                            messages.error(request, f"La nota para {record.name} ({record.date}) debe estar entre 2 y 5.")
                            error = True
                    except ValueError:
                        messages.error(request, f"Nota inválida para {record.name} ({record.date}).")
                        error = True
                else:
                    messages.error(request, f"Debes ingresar una nota para {record.name} ({record.date}).")
                    error = True
            if not error:
                messages.success(request, "Cambios de evaluaciones guardados exitosamente.")

        storage = get_messages(request)
        message_list = [{"text": m.message, "tag": m.tags} for m in storage]
        if error:
            return JsonResponse({"success": False, "messages": message_list}, status=400)
        return JsonResponse({"success": True, "messages": message_list})

    context = {
        'subject': subject,
        'student': student,
        'attendance_records': attendance_records,
        'grade_records': grade_records,
    }
    return render(request, 'professor/student_subject_detail.html', context)


@login_required
@student_required
def student_dashboard(request: HttpRequest):
    student: Student = request.user.student

    subjects = Subject.objects.filter(
            career=student.career,
            year=student.academic_year
    ).order_by('year', 'name')  

    subject_data = []
    for subject in subjects:
        grades = GradeRecord.objects.filter(student=student, subject=subject)
        grade_avg = grades.aggregate(avg=models.Avg('grade'))['avg']
        grade_avg = round(float(grade_avg), 1) if grade_avg is not None else "N/A"

        attendances = AttendanceRecord.objects.filter(student=student, subject=subject)
        total_attendance = attendances.count()
        if total_attendance > 0:
            attended_count = attendances.filter(attended=True).count()
            attendance_percent = round((attended_count / total_attendance) * 100, 1)
            attendance_display = f"{attendance_percent}%"
        else:
            attendance_display = "N/A"

        subject_data.append({
            'subject': subject,
            'grade_avg': grade_avg,
            'attendance': attendance_display,
            'has_grades': grades.exists(),
            'has_attendance': attendances.exists(),
        })

    comments = Comment.objects.filter(
        student__user=student.user
    ).order_by('-date')

    context = {
        'comments': comments,
        'subject_data': subject_data,
    }

    return render(request, 'student/student_dashboard.html', context)


@login_required
@student_required
def subject_register_detail(request: HttpRequest, subject_id: int):
    student = request.user.student
    subject = get_object_or_404(Subject, id=subject_id)

    attendance_records = AttendanceRecord.objects.filter(subject=subject, student=student).order_by('-date')
    grade_records = GradeRecord.objects.filter(subject=subject, student=student).order_by('-date', 'name')

    context = {
        'subject': subject,
        'attendance_records': attendance_records,
        'grade_records': grade_records,
    }
    return render(request, 'student/subject_register_detail.html', context)