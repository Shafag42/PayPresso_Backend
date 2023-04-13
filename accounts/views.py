from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import PersonalUser,BusinessUser,Profile
from rest_framework import generics,permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView
from .serializers import PersonalUserSerializer, BusinessUserSerializer, TokenObtainPairSerializer,LoginSerializer,LogoutSerializer,BusinessUserProfileSerializer,PersonalUserProfileSerializer

@permission_classes([permissions.AllowAny])
class PersonalUserRegisterView(CreateAPIView):
    serializer_class = PersonalUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': True,
            'status code': status.HTTP_200_OK,
            'message': 'Personal user registered successfully'
        }
        return Response(response, status=status.HTTP_200_OK)


@permission_classes([permissions.AllowAny])
class BusinessUserRegisterView(CreateAPIView):
    serializer_class = BusinessUserSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': True,
            'status code': status.HTTP_200_OK,
            'message': 'Business user registered successfully'
        }
        return Response(response, status=status.HTTP_200_OK)

@permission_classes([permissions.AllowAny])
class UserLoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        personal_user = PersonalUser.objects.filter(email=email).first()
        business_user = BusinessUser.objects.filter(email=email).first()

        if personal_user is None and business_user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if personal_user is not None:
            user = personal_user.user
        else:
            user = business_user.user

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
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = RefreshToken(serializer.validated_data['refresh'])
            refresh_token.blacklist()
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Successfully logged out.'}, status=status.HTTP_200_OK)

class TokenObtainPairWithUserTypeView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data.get('access')

        if token:
            decoded_token = RefreshToken(token).payload
            user_type = decoded_token.get('user_type')

            if user_type == 'personal':
                response.data['user_type'] = 'personal'
            elif user_type == 'business':
                response.data['user_type'] = 'business'

        return response
    
@permission_classes([permissions.IsAuthenticated])
class PersonalUserProfileView(CreateAPIView):
    serializer_class = PersonalUserProfileSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        profile_serializer = self.serializer_class(data=request.data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save(user=user)
        return Response(profile_serializer.data)

@permission_classes([permissions.IsAuthenticated])
class PersonalUserProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = PersonalUserProfileSerializer

    def get_object(self):
        user = self.request.user
        return Profile.objects.get(user=user)

@permission_classes([permissions.IsAuthenticated])
class BusinessUserProfileView(CreateAPIView):
    serializer_class = BusinessUserProfileSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        profile_serializer = self.serializer_class(data=request.data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save(business_user=user)
        return Response(profile_serializer.data)

@permission_classes([permissions.IsAuthenticated])
class BusinessUserProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = BusinessUserProfileSerializer

    def get_object(self):
        user = self.request.user
        return Profile.objects.get(business_user=user)

# -------------------------------------------------------------------

# class PersonalProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#     queryset = PersonalProfile.objects.all()
#     serializer_class = PersonalProfileSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_object(self):
#         return PersonalProfile.objects.get(user=self.request.user)
    
    # def put(self, request, *args, **kwargs):
    #     profile = self.get_object()
    #     serializer = self.get_serializer(profile, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)


# class BusinessProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#     queryset = BusinessProfile.objects.all()
#     serializer_class = BusinessProfileSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_object(self):
#         return BusinessProfile.objects.get(user=self.request.user)


# class UserLoginView(RetrieveAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserLoginView

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         response = {
#             'success' : 'True',
#             'status code' : status.HTTP_200_OK,
#             'message': 'User logged in  successfully',
#             'token' : serializer.data['token'],
#             }
#         status_code = status.HTTP_200_OK

#         return Response(response, status=status_code)