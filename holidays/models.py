from django.db import models


# Create your models here.

class Hollidays(models.Model):
    name = models.CharField(max_length=100)
    dita = models.DateField(blank=False, null=False)

    def __str__(self):
        return self.name