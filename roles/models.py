from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Rolet(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    name = models.CharField(max_length=50)
    roli = models.ForeignKey(Rolet, on_delete=models.CASCADE, related_name='Roli')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_role')

    def __str__(self):
        return self.name

    def is_hr(self):
        return self.roli

