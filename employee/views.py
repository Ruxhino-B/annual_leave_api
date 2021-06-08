from django.shortcuts import render
from rest_framework.response import Response
from .models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Employee
from .serializers import EmployeeSerializers
from .permissions import ReadOnly, HrOrReadOnly, ReadOnlyHimselfsOrIsHr


# CreateAPIView ==> Vetem krijon Create dhe nuk shikon detaje
# ListAPIView ==> Shikon listen
# RetriveAPIView ==> Shikon details
# DestroyeAPIView ==> Fshin/Delete element
# UpdateAPIView ==> vetem ben update

# ListCreateAPIView --> Liston dhe krijon Api view
# RetriveUpdateAPIView ==> Shikon/Updateon API
# RetriveDestroyAPIView ==> shikon/fshin API View
# RetrieveUpdateDestroyAPIView ==> shikon/Updaten/Fshin ApiView

class EmployeeSerializerListView(generics.ListCreateAPIView):
    """Create and List element of all Employees"""
    serializer_class = EmployeeSerializers
    queryset = Employee.objects.all()
    permission_classes = [HrOrReadOnly]

    # def get_queryset(self):
    #     useri = self.request.user.id
    #     return Employee.objects.all()


class EmployeeSerializerCreateApiView(generics.CreateAPIView):
    serializer_class = EmployeeSerializers
    queryset = Employee.objects.all()
    permission_classes = [HrOrReadOnly]


class EmployeeSerializerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View Detail on Employee, Update, Delete """
    serializer_class = EmployeeSerializers

    permission_classes = [ReadOnlyHimselfsOrIsHr]
    queryset = Employee.objects.all()

    def delete(self, request, *args, **kwargs):
        emp_pk = kwargs['pk']
        emp = User.objects.get(id=emp_pk)
        emp.is_active = False
        emp.save()
        return Response({"message":f"{emp.username} is Deactivate as User {emp.is_active}"})

class EmployeeSerializerDetailViewHimself(generics.ListAPIView):
    serializer_class = EmployeeSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        req_employee = User.objects.get(id=user.id)
        return Employee.objects.filter(user_id=req_employee)

class EmployeeSerializerUpdateDeleteRetrive(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeSerializers
    permission_classes = [ReadOnlyHimselfsOrIsHr & HrOrReadOnly]
    queryset = Employee.objects.all()