from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import  MyUserSerializer,PersonalProfileSerializer, BusinessProfileSerializer,MyTokenObtainPairSerializer
from accounts.models import MyUser,PersonalProfile,BusinessProfile
from rest_framework import generics,permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate


class MyUserCreateView(generics.CreateAPIView):
    queryset =MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (permissions.AllowAny,)


class PersonalProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = PersonalProfile.objects.all()
    serializer_class = PersonalProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return PersonalProfile.objects.get(user=self.request.user)
    
    def put(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class BusinessProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return BusinessProfile.objects.get(user=self.request.user)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@permission_classes([permissions.AllowAny])
class LoginView(APIView):
    """View for user login."""
    def post(self, request, format=None):
        serializer = MyTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([permissions.IsAuthenticated])
class LogoutView(APIView):
    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data["refresh_token"]
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out."},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Error logging out."},status=status.HTTP_400_BAD_REQUEST)



# class PersonalRegistrationView(CreateAPIView):

#     serializer_class = PersonalRegistrationSerializer
#     permission_classes = (AllowAny,)

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         response = {
#             'success' : 'True',
#             'status code' : status.HTTP_200_OK,
#             'message': 'Paitent registered  successfully',
#             }
#         status_code = status.HTTP_200_OK
#         return Response(response, status=status_code)

# class BusinessRegistrationView(CreateAPIView):

    # serializer_class = BusinessRegistrationSerializer
    # permission_classes = (AllowAny,)

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     response = {
    #         'success' : 'True',
    #         'status code' : status.HTTP_200_OK,
    #         'message': 'Businness account registered  successfully',
    #         }
    #     status_code = status.HTTP_200_OK
    #     return Response(response, status=status_code)

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