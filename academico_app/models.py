from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from enum import Enum

class UserRole(Enum):
    ADMIN = 'admin'
    PROFESSOR = 'professor'
    STUDENT = 'student'

class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password):
        if not username:
            raise ValueError("El usuario debe tener un nombre de usuario")
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password=None):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True  
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True, db_index=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False) 

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
    
    def get_role(self) -> UserRole:
        
        for item in UserRole:
            if (item == UserRole.ADMIN):
                if self.is_admin: return item
            elif hasattr(self, item.value): return item
        
        raise ValueError("No se ha añadido dicho rol al enum de roles de usuario")
    
    def is_professor(self):
        return hasattr(self, 'professor')

    def is_student(self):
        return hasattr(self, 'student')
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_staff(self):
        return self.is_admin


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.username})"
    
    def clean(self):
        if hasattr(self.user, 'student'):
            raise ValidationError("Este usuario ya está registrado como estudiante.")
        
        super().clean()


class Student(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    career = models.ForeignKey('Career', on_delete=models.CASCADE, related_name='students')
    academic_year = models.IntegerField(
        validators=[
            MinValueValidator(1, message="El año escolar no puede ser menor a 1."),
            MaxValueValidator(4, message="El año escolar no puede ser mayor a 4.")
        ],
    )


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.username})"
    
    def clean(self):
        if hasattr(self.user, 'professor'):
            raise ValidationError("Este usuario ya está registrado como profesor.")
        super().clean()
    
    
class Career(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=50)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='career_subject')
    
    year = models.IntegerField(
        validators=[
            MinValueValidator(1, message="El año escolar no puede ser menor a 1."),
            MaxValueValidator(4, message="El año escolar no puede ser mayor a 4.")
        ],
    )
    
    completed = models.BooleanField(default=False)
    
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name='professor_subject')

    def __str__(self):
        return self.name


class GradeRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_register')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_register')
    
    grade = models.DecimalField(
        max_digits=3, decimal_places=1,  
        validators=[MinValueValidator(2), MaxValueValidator(5)],
        null=True, blank=True,
    )

    date = models.DateField() 
    name = models.CharField(max_length=255)  

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(grade__range=(0, 5)), name='valid_grade'),
        ]

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.date})"

class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_attendance')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_attendance')
    
    attended = models.BooleanField()  
    date = models.DateField()  

    def __str__(self):
        status = "Asistió" if self.attended else "Faltó"
        return f"{self.student} - {self.subject} ({self.date}) - {status}"


class Comment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_comment')
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name='professor_comment')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.professor} - {self.student}"
