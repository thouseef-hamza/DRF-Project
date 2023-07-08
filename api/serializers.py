from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# User = get_user_model()


class UserRegister(serializers.ModelSerializer):
    first_name=serializers.CharField(style={"input":"text"},write_only=True)
    last_name = serializers.CharField(style={'input':'text'},write_only=True)
    password2 = serializers.CharField(style={'input':'password'},write_only = True)
    
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password','password2']    
    
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Has Been ALready Used")
        return value
        
    def save(self):
        user=User(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2=self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'password':'Password Does Not Match'})
        user.set_password(password)
        user.save()
        return user
        