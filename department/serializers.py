from rest_framework import  serializers
from .models import Department

class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'parent_department', 'name')
        model = Department
