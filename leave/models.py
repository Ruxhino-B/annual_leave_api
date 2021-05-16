import datetime

from django.db import models
from employee.models import Employee

# Create your models here.

class Leje(models.Model):
    name = models.CharField(max_length=50)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_id')
    fillim_leje = models.DateTimeField(auto_now_add=True)
    fund_leje = models.DateTimeField(default=datetime.timedelta(hours=4))
    def __str__(self):
        return self.name