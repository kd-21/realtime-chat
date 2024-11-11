from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('rooms/', rooms, name='rooms'),   
    path('room/<slug:slug>/', room, name='room'),
    # path('edit/', profile_edit_view, name='profile-edit'),
    
]







# accounts/login/ 
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']