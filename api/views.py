from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegister
from rest_framework.response import Response
from rest_framework.authtoken.models import Token  
from rest_framework.permissions import IsAuthenticated
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