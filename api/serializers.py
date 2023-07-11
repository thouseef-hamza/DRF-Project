from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    profile_picture=serializers.ImageField(required=False   )
    class Meta:
        model =User
        fields=['email','username','password','password2','tc','profile_picture']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password Does Not Match")
        return attrs
    
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=200)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','username']