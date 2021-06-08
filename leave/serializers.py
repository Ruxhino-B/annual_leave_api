from .models import Leje, ApprovimLeje
from rest_framework import serializers
from employee.serializers import EmployeeSerializers

class LejeSerializers(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'employee_id', 'fillim_leje', 'fund_leje')
        #read_only_fields = ('employee_id',)
        model = Leje
        depth = 1

class PranimRefuzimSerializers(serializers.ModelSerializer):
    status = serializers.BooleanField(default=False)
    #leje = LejeSerializers(many=True, read_only=True)
    class Meta:
        fields = ('name', 'koment', 'status', 'leje', 'manager')
        model = ApprovimLeje