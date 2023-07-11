from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('',views.registration,name='register'),
    path('login/',views.signIn,name='login'),    
    path('user_detail/<int:pk>/',views.user_detail,name='user_detail'),    
    path('user_profile/',views.user_profile,name='user_profile'),    
]
 