# accounts/urls.py
from django.urls import path
from .views import SignUpView,login

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('login/', login, name='login'),
    # path('logout/', user_logout, name='logout')
    
]