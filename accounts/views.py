from http.client import NOT_FOUND
from rest_framework import status,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import CustomUser
from rest_framework import permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView
from .serializers import (CustomUserSerializer,CustomTokenObtainPairSerializer,UserProfileSerializer,
                          LoginSerializer,ResetPasswordSerializer,ForgotPasswordSerializer)
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator

token_generator = PasswordResetTokenGenerator()




@permission_classes([permissions.AllowAny])
class CustomUserRegisterView(CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        # serializer = self.serializer_class(data=request.data)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': True,
            'status code': status.HTTP_200_OK,
            'message': 'User registered successfully'
        }
        return Response(response, status=status.HTTP_200_OK)
    
   
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = super().post(request, *args, **kwargs)
        return Response({
            'refresh': response.data['refresh'],
            'access': response.data['access'],
            'user_id': serializer.user.id,
            'email': serializer.user.email
        }, status=status.HTTP_200_OK)
    
@permission_classes([permissions.IsAuthenticated])
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    # def get_object(self):
    #     return self.request.user
    def get_object(self):
        user = self.request.user
        # try:
        #     profile = CustomUser.objects.get(user=user)
        # except CustomUser.DoesNotExist:
        #     raise NOT_FOUND("Profile not found")
        return user


@permission_classes([permissions.AllowAny])
class UserLoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = CustomUser.objects.filter(email=email).first()
        
        if user is None :
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        response_data = {
            'user_id': user.id,
            'email': user.email,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
@permission_classes([permissions.IsAuthenticated])
class LogoutView(APIView):

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})
    
@permission_classes([permissions.IsAuthenticated])
class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = CustomUser.objects.filter(email=email).first() 
        if not user:
            return Response({'error': 'No user with this email address found'},
                            status=status.HTTP_404_NOT_FOUND)
        

        # token = user.get_password_reset_token()
        token = token_generator.make_token(user)
        reset_link = request.build_absolute_uri(reverse('reset-password')) + '?token=' + token

        # send email to the user with the password reset link
        subject = 'Password reset link'
        message = f'Hello,\n\nPlease use the following link to reset your password:\n\n{request.build_absolute_uri(reverse("reset-password"))}\n\nBest regards,\nYour App team'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return Response({'success': 'Password reset link has been sent to your email address'},
                        status=status.HTTP_200_OK)
    

class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        user = request.user
        password = serializer.validated_data['password']

        new_password = serializer.validated_data['password']
        confirm_password = serializer.validated_data['confirm_password']
        if new_password != confirm_password:
            return Response(
                {"error": "New password and confirm password does not match."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(password)
        user.save()
    
        # Send email notification to the user
        subject = "Your password has been changed"
        message = f"Hello {user.email},\n\nYour password has been changed successfully."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        response = {
            'success': True,
            'status code': status.HTTP_200_OK,
            'message': 'Password reset successful'
        }
        return Response(response, status=status.HTTP_200_OK)