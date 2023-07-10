from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer,UserLoginSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token  
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from django.contrib.auth import authenticate
from .renderers import UserRenderer
# Create your views here.

class UserRegistrationView(APIView): 
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            return Response({"msg":"Registered Successfully"},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

registration = UserRegistrationView.as_view()

class UserLoginView(APIView):
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                return Response({"msg":"Login Success"},status=status.HTTP_200_OK)
            else:
                return Response({"errors":{'non_field_errors':['Email Or Password is Not Valid']}},status=status.HTTP_404_NOT_FOUND )
            
signIn = UserLoginView.as_view()

# class TokenAuth(APIView):
#     permission_classes = (IsAuthenticated,)
    
#     def get(self,request):
#         content={'user':str(request.user),'user_id':str(request.user.id)}
#         return Response(content)
   

# success = TokenAuth.as_view()

# class UserDetail(APIView):
#     permission_classes=[IsAdminUser]
#     def get_object(self,pk):
#         try:
#             return User.objects.get(pk=pk)
#         except:
#             raise Http404
    
#     def get(self,request,pk,format=None):
#         user_data = self.get_object(pk)
#         serializer=UserDataSerializer(user_data)
#         return Response(serializer.data)
    
#     def put(self,request,pk,format=None):
#         user_data = self.get_object(pk)
#         serializer=UserDataSerializer(user_data,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response({"message":"Invalid Credentials","Error":serializer.errors})
    
#     def delete(self,request,pk,format=None):
#         user_data = self.get_object(pk)
#         user_data.delete()
#         return Response({"message":"User Deleted Successfully"})
    
        
# user_detail = UserDetail.as_view()
