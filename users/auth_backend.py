from django.contrib.auth.backends import ModelBackend
from .models import User

class StudentIDAuthBackend(ModelBackend):
    def authenticate(self, request, studentID=None, password=None, **kwargs):
        try:
            user = User.objects.get(studentID=studentID)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
