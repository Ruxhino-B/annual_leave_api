from django.db import models

# Create your models here.

class Department(models.Model):
    parent_department = models.ForeignKey("Department", blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
