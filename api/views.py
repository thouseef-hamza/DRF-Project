from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token  
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status,viewsets
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework import generics
# Create your views here.

#  Generate Token Manually

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    
class UserRegistrationView(APIView): 
    # permission_classes=[IsAdminUser]
    renderer_classes = [UserRenderer]
    
    def get(self,request,format=None):
        user=User.objects.all()
        serializer = UserRegistrationSerializer(user,many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            print(user)
            return Response({"Token":token,"msg":"Registered Successfully"},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

registration = UserRegistrationView.as_view()

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({"Token":token,"msg":"Login Success"},status=status.HTTP_200_OK)
            else:
                return Response({"errors":{'non_field_errors':['Email Or Password is Not Valid']}},status=status.HTTP_404_NOT_FOUND )
            
signIn = UserLoginView.as_view()

class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
user_profile = UserProfileView.as_view()


class UserDetail(APIView):
    # permission_classes=[IsAdminUser]
    
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise Http404
    
    def get(self,request,pk=None,format=None):
        user_data = self.get_object(pk)
        serializer=UserProfileSerializer(user_data)
        return Response(serializer.data)

    
    def put(self,request,pk,format=None):
        user_data = self.get_object(pk)
        serializer=UserProfileSerializer(user_data,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"message":"Invalid Credentials","Error":serializer.errors})
    
    def delete(self,request,pk,format=None):
        user_data = self.get_object(pk)
        user_data.delete()
        return Response({"message":"User Deleted Successfully"})
    
        
user_detail = UserDetail.as_view()
