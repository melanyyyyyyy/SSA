from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('login/check/', views.login_check, name='login_check'),
    path('logout/', views.logout_view, name='logout'),
    path('professor/dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('professor/dashboard/<int:subject_id>', views.subject_view, name='subject_view'),
    path('professor/dashboard/attendance/<int:subject_id>', views.register_attendance, name='register_attendance'),
    path('professor/dashboard/grade/<int:subject_id>', views.register_grade, name='register_grade'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit-comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('professor/dashboard/<str:username>/comment/cancel/', views.cancel_comment, name='cancel_comment'),
    path('professor/dashboard/comment/<str:username>/<int:subject_id>/', views.comment_add, name='comment_add'),
    path('professor/dashboard/history/<int:subject_id>/', views.history, name='history'),
    path('professor/dashboard/history/delete_attendance/', views.delete_attendance_record, name='delete_attendance_record'),
    path('professor/dashboard/history/delete_grade/', views.delete_grade_record, name='delete_grade_record'),
    path('professor/dashboard/history/attendance/<int:subject_id>/<str:date>/', views.history_detail_attendance, name='history_detail_attendance'),
    path('professor/dashboard/history/grade/<int:subject_id>/<str:date>/<str:name>/', views.history_detail_grade, name='history_detail_grade'),
    path('professor/dashboard/subject/<int:subject_id>/student/<int:student_id>/details/', views.student_subject_detail, name='student_subject_detail'),
    path('student/dashboard/', views.student_dashboard, name = 'student_dashboard'),
    path('student/subject/<int:subject_id>/detail/', views.subject_register_detail, name='subject_register_detail'),
]

