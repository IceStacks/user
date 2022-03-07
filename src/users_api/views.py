from urllib import request
from rest_framework import generics
from rest_framework.permissions import BasePermission
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer

class IsCustomerAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and
                    request.user.groups.filter(name='Customer Admins'))

class UserList(generics.ListCreateAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegister(generics.CreateAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    
    
    