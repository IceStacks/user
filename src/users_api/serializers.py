from rest_framework import serializers
from .models import User

#empty fields turns string instead null. why?
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name',
                  'gender', 'country', 'town', 'address',
                  'phone_number', 'identity_number',
                  'birth_date', 'is_active', 'is_staff','is_superuser')
        extra_kwargs ={'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user
    
        
    #if field is empty string return null 
    #implement this if form returns an empty string.
    #https://stackoverflow.com/questions/44717442/this-querydict-instance-is-immutable
    # def to_internal_value(self, data):
    #     my_fields = self.Meta.fields
    #     _mutable = data._mutable
    #     data._mutable = True
    #     for field in my_fields:
    #         if data.get(field, None) == '':
    #             data.pop(field)
    #     data._mutable = _mutable
    #     return super(UserSerializer, self).to_internal_value(data) 
