import datetime
import timedelta

from django.db import models
from employee.models import Employee
from django.contrib.auth.models import User

# Create your models here.

class Leje(models.Model):
    name = models.CharField(max_length=50)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_id')
    fillim_leje = models.DateTimeField(auto_now_add=True)
    fund_leje = models.DateTimeField()
    def __str__(self):
        return self.name

class ApprovimLeje(models.Model):
    name = models.CharField(max_length=50)
    koment = models.TextField()
    status = models.BooleanField()
    leje = models.OneToOneField(Leje, on_delete=models.CASCADE, related_name='leje_set', primary_key=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager_set')

    def __str__(self):
        return self.name
