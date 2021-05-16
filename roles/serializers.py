from rest_framework import serializers
from .models import Rolet, UserRole

class RoleSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ('id','name')
        model = Rolet

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id','name','roli','user_id')
        model = UserRole