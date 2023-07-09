from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('',views.registration,name='register'),
    path('login/',obtain_auth_token,name='login'),    
    path('success/',views.success,name='success'),    
    path('user_detail/<int:pk>/',views.user_detail,name='user_detail'),    
    path('user_delete/<int:id>/',views.user_delete,name='user_delete'),    
]
