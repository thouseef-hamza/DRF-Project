from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegister,UserDataSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token  
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
# Create your views here.

class register(APIView):
    
    def post(self,request,format=None):
        serializer = UserRegister(data=request.data)
        data={}
        if serializer.is_valid():
            Accounts = serializer.save()
            data['response'] = 'Your Account Registered Succesfully'
            token,create = Token.objects.get_or_create(user=Accounts)
            data['token'] = token.key
        else:
            data = serializer.errors
        return Response(data)

registration = register.as_view()

class TokenAuth(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        content={'user':str(request.user),'user_id':str(request.user.id)}
        return Response(content)
   

success = TokenAuth.as_view()

class UserDetail(APIView):
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise Http404
    
    def get(self,request,pk,format=None):
        user_data = self.get_object(pk)
        serializer=UserDataSerializer(user_data)
        return Response(serializer.data)
    
    def put(self,request,pk,format=None):
        user_data = self.get_object(pk)
        serializer=UserDataSerializer(user_data,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"message":"Invalid Credentials","Error":serializer.errors})
    
    def delete(self,request,pk,format=None):
        user_data = self.get_object(pk)
        user_data.delete()
        return Response({"message":"User Deleted Successfully"})
    
        
            

user_detail = UserDetail.as_view()

class UserDelete(APIView):
    pass

user_delete = UserDelete.as_view()