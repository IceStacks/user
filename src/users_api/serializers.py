from asyncio.windows_events import NULL
from tkinter.ttk import Style
from rest_framework import serializers
from .models import User

#empty fields turns string instead null. why?
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'gender', 'country', 'town', 'address',
                  'phone_number', 'identity_number',
                  'birth_date', 'is_active', 'is_staff','is_superuser')

    #if field is empty string return null
    def to_internal_value(self, data):
        my_fields = self.Meta.fields
        for field in my_fields:
            if data.get(field, None) == '':
                data.pop(field)
        return super(UserSerializer, self).to_internal_value(data)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        user.set_password(password)
        user.save()
        return user




    

