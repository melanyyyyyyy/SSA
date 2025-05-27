from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('login/check/', views.login_check, name='login_check'),
    path('logout/', views.logout_view, name='logout'),
    
    path('dashboard/professor/', views.professor_dashboard, name='professor_dashboard'),
    
    path('professor/subject/<int:subject_id>', views.subject_view, name='subject_view'),
    path('professor/attendance/<int:subject_id>', views.register_attendance, name='register_attendance'),
    path('professor/grade/<int:subject_id>', views.register_grade, name='register_grade'),
    
    path('professor/comments/add/<str:username>/<int:subject_id>/', views.comment_add, name='comment_add'),
    path('professor/comments/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('professor/comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('professor/comments/cancel/<str:username>/', views.cancel_comment, name='cancel_comment'),
    
    path('professor/history/<int:subject_id>/', views.history, name='history'),
    path('professor/history/delete_attendance/', views.delete_attendance_record, name='delete_attendance_record'),
    path('professor/history/delete_grade/', views.delete_grade_record, name='delete_grade_record'),
    path('professor/history/attendance/<int:subject_id>/<str:date>/', views.history_detail_attendance, name='history_detail_attendance'),
    path('professor/history/grade/<int:subject_id>/<str:date>/<str:name>/', views.history_detail_grade, name='history_detail_grade'),
    
    path('professor/student_subject_info/<int:subject_id>/<int:student_id>/', views.student_subject_detail, name='student_subject_detail'),
    
    path('dashboard/student/', views.student_dashboard, name = 'student_dashboard'),
    path('student/subject/<int:subject_id>/detail/', views.subject_register_detail, name='subject_register_detail'),
]

