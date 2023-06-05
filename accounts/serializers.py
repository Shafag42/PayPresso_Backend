from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import CustomUser
from datetime import datetime,date


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    # birthday = serializers.DateField(format='%d.%m.%Y')
    
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password','confirm_password' ,'is_personal', 'is_business',
                  'first_name', 'last_name', 'phone_number', 'birthday', 'company_name', 'voen']
        extra_kwargs = {'password': {'write_only': True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial_data.get('is_personal') == True:
            self.fields['email'].required = True
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            self.fields['phone_number'].required = True
            self.fields['birthday'].required = True
        elif self.initial_data.get('is_business') == True:
            self.fields['email'].required = True
            self.fields['phone_number'].required = True
            self.fields['company_name'].required = True
            self.fields['voen'].required = True
            self.fields['first_name'].required = False  # Make first_name optional
            self.fields['last_name'].required = False  # Make last_name optional

        # Check for business_user or personal_user query parameter
        # if self.context['request'].GET.get('is_business'):
        if self.context.get('request') and self.context['request'].GET.get('is_business'):
            self.fields['email'].required = True
            self.fields['phone_number'].required = True
            self.fields['company_name'].required = True
            self.fields['voen'].required = True
            self.fields['first_name'].required = False  # Make first_name optional
            self.fields['last_name'].required = False  # Make last_name optional
        # elif self.context['request'].GET.get('is_personal'):
        elif self.context.get('request') and self.context['request'].GET.get('is_personal'):
            self.fields['email'].required = True
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            self.fields['phone_number'].required = True
            self.fields['birthday'].required = True
        

    
    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

    
        is_personal = validated_data.pop('is_personal',False)
        is_business = validated_data.pop('is_business',False)

        if is_personal and not is_business:
            user = CustomUser.objects.create_user(
                email=validated_data.pop('email'),
                password=password,
                is_personal=True,
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                phone_number=validated_data['phone_number'],
                birthday=validated_data['birthday']
                
            )
        elif is_business and not is_personal:
            user = CustomUser.objects.create_user(
                email=validated_data.pop('email'),
                password=password,
                phone_number=validated_data['phone_number'],
                company_name=validated_data['company_name'],
                voen=validated_data['voen'],
                is_business=True
            )
        else:
            raise serializers.ValidationError({'is_personal': 'Choose one account type.'})
        return user

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        user = get_user_model().objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError('User not found')

        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password')

        if not user.is_active:
            raise serializers.ValidationError('User is inactive')

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'last_name', 'first_name', 'phone_number', 'birthday', 'company_name', 'voen','password']
        read_only_fields = ['email','company_name','voen','birthday']

    def to_representation(self, instance):
        if instance.is_business:
            # self.fields['company_name'].read_only = False
            self.fields['password'].read_only = False
        if instance.is_personal:
            # self.fields['company_name'].read_only = False
            self.fields['password'].read_only = False
        return super().to_representation(instance)



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

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


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        User = get_user_model()
        try:
            user = User.objects.get(email=value)
            if not user.is_personal and not user.is_business:
                raise serializers.ValidationError("User not found")
        except User.DoesNotExist:
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

