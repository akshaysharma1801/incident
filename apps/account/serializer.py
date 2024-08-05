from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """ Register a new user serializer. """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 
                'first_name', 'last_name', 'phone_number', 
                'address', 'city', 'state', 'country')


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],
            city=validated_data['city'],
            state=validated_data['state'],
            country=validated_data['country']
        )
        return user
    
class UserDetailSerializer(serializers.ModelSerializer):
    """ Get basic details of user serializer. """

    class Meta:
        model = User
        exclude = ['password', 'last_login','is_staff', 'is_superuser']

class LoginSerializer(serializers.Serializer):
    """ Login a user in system serializer.

    Serializer will autehnticate and generate the JWT token 
    for a user after login.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        request = self.context.get('request')

        if email and password:
            user = authenticate(request=request, email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include "email" and "password"')

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        user_detail = UserDetailSerializer(user)
        return {
            'details':user_detail.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }