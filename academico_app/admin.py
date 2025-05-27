from django.contrib import admin
from .models import User, Professor, Student, Career, Subject, GradeRecord, AttendanceRecord, Comment
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_active', 'is_admin')

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('username', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name')}),
        ('Permisos', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'career', 'academic_year')
    autocomplete_fields = ['user']  
    search_fields = ('user__first_name', 'user__last_name', 'career__name')

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user',)
    autocomplete_fields = ['user']  
    search_fields = ('user__first_name', 'user__last_name')

class CareerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'career', 'year', 'professor', 'completed')
    list_filter = ('career', 'year',)
    search_fields = ('name',)
    autocomplete_fields = ('professor',)  
    
class GradeRecordAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        return False
    
    list_display = ('student', 'subject', 'grade', 'date')
    list_filter = ('subject__career', 'subject__year',)  
    search_fields = ('student__user__username', 'subject__name')
    
class AttendanceRecordAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        return False
    
    list_display = ('student', 'subject', 'attended', 'date')
    list_filter = ('subject__career', 'subject__year',)  
    search_fields = ('student__user__username', 'subject__name')


class CommentAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request):
        return False
    
    list_display = ('student', 'professor', 'date', 'comment')
    readonly_fields = ('date',)


admin.site.register(User, UserAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Career, CareerAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(GradeRecord, GradeRecordAdmin)
admin.site.register(AttendanceRecord, AttendanceRecordAdmin)

admin.site.unregister(Group)