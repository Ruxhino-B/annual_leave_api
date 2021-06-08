from .models import Hollidays
from rest_framework import serializers

class HolidaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hollidays
        fields = ('id', 'name', 'dita')