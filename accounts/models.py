from django.contrib.auth.models import AbstractUser
#abstract user is the inbuilt class allowing us to override our custom auth django set up
from django.db import models
# Create your models here.
class User(AbstractUser):
    # constant varible
    # user roles
    USER_TYPE_ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    #table columns
    user_type = models.CharField(max_length = 10, choices=USER_TYPE_ROLES)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    #methods to act on the attributes
    def __str__(self):
        f"{self.username} - {self.email}"
    ##metthod to return the user role
    def is_teacher(self):
        return self.user_type == 'teacher' #true oe false
    def is_student(self):
        return self.user_type == 'student' #true or false       