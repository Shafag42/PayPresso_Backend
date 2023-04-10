from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import MyUser,PersonalProfile,BusinessProfile


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ( "email", "password", "is_personal", "is_business")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = MyUser.objects.create_user(password=password, **validated_data)
        return user
    
class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class PersonalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalProfile
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)
            
            if user.is_superuser:
                token['is_superuser'] = True
                
                return token

# class BusinessRegistrationSerializer(serializers.ModelSerializer):
    # profile = BusinessProfileSerializer(required=False)

    # class Meta:
    #     model = MyUser
    #     fields = ('email', 'password', 'profile')
    #     extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     user = MyUser.objects.create_businessuser(**validated_data)
    #     BusinessProfile.objects.create(
    #         user=user,
    #         first_name=profile_data['first_name'],
    #         last_name=profile_data['last_name'],
    #         phone_number=profile_data['phone_number'],
    #         #age=profile_data['age'],
            
    #     )
    #     return user

# class PersonalRegistrationSerializer(serializers.ModelSerializer):

#     profile = PersonalProfile(required=False)

#     class Meta:
#         model = MyUser
#         fields = ('email', 'password', 'profile')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile')
#         user = MyUser.objects.create_personaluser(**validated_data)
#         PersonalProfile.objects.create(
#             user=user,
#             first_name=profile_data['first_name'],
#             last_name=profile_data['last_name'],
#             phone_number=profile_data['phone_number'],
            
#         )
#         return user
    

    

