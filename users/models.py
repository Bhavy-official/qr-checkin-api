from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, studentID, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not studentID:
            raise ValueError("Student ID is required")
        if not full_name:
            raise ValueError("Full name is required")
        email = self.normalize_email(email)
        user = self.model(email=email, studentID=studentID, full_name=full_name, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, studentID, full_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, studentID, full_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("host", "Host"),
    )

    email = models.EmailField(unique=True)
    studentID = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)  # ✅ Added full_name
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["studentID", "full_name"]  # ✅ Include full_name

    def __str__(self):
        return f"{self.full_name} ({self.email})"

