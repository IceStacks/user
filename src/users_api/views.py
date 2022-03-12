from rest_framework import generics
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .serializers import UserSerializer
from core.settings import SECRET_KEY
import jwt, datetime

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


class UserRegister(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserLogin(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            'iat': datetime.datetime.utcnow()
        }

        #str cant be decoded error fixed by downgrading to jwt==1.7.1
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
    
class UserLogout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response