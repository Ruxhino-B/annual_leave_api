from django.db import models
from django.contrib.auth.models import User
from department.models import Department
from roles.models import User, UserRole

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='e_user', primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='e_department')

    def __str__(self):
        return self.name



