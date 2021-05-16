from rest_framework import serializers
from .models import Employee

class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ('user_id','name', 'department')
        model = Employee
