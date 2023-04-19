from django.contrib.auth import authenticate
from rest_framework import serializers
# from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import PersonalUser,BusinessUser,PersonalProfile,BusinessProfile
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class PersonalUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = PersonalUser
        fields = ['id', 'email','first_name', 'last_name','birthday','phone_number','password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        if 'confirm_password' in validated_data:
            validated_data.pop('confirm_password')
        return PersonalUser.objects.create_user(**validated_data)

class BusinessUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = BusinessUser
        fields = ['id', 'email', 'company_name', 'voen', 'phone_number', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return BusinessUser.objects.create_user(**validated_data)
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    # confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password')
        else:
            raise serializers.ValidationError('Email and password are required')

        attrs['user'] = user
        return attrs
    

# class LogoutSerializer(serializers.Serializer):
#     refresh = serializers.CharField()

#     def validate(self, attrs):
#         self.token = attrs['refresh']
#         return attrs

#     def save(self, **kwargs):
#         try:
#             RefreshToken(self.token).blacklist()
#         except Exception as e:
#             raise serializers.ValidationError('Invalid token')
        

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        if isinstance(user, PersonalUser):
            token['user_type'] = 'personal'
        elif isinstance(user, BusinessUser):
            token['user_type'] = 'business'

        return token


class PersonalUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalProfile
        fields = ['phone_number', 'birthday']
        extra_kwargs = {'password': {'write_only': True}}


class BusinessUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = ['phone_number', 'company_name', 'voen']
        extra_kwargs = {'password': {'write_only': True}}

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            PersonalUser.objects.get(email=value)
        except PersonalUser.DoesNotExist:
            try:
                BusinessUser.objects.get(email=value)
            except BusinessUser.DoesNotExist:
                raise serializers.ValidationError("User not found")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

