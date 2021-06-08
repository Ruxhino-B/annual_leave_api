from rest_framework import  serializers
from .models import Department

class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'parent_department', 'name')
        model = Department

# class DepartmentSerializerHyperlink(serializers.HyperlinkedModelSerializer):
#     #url = serializers.HyperlinkedIdentityField(view_name='DetailView', lookup_field='id')
#     class Meta:
#         model = Department
#         fields = ('id', 'parent_department', 'name', 'url')
