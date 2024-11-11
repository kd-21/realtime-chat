from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, CustomLoginForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm  
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import logout
from django.http import JsonResponse



@login_required(login_url='login') 
def home(request):
    return render(request, 'home.html')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    



def invalidate_other_sessions(user):
    # Get all sessions for the user
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(user.id):
            session.delete()  # Delete the session to log out

def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():        
            user = form.get_user()
            # Invalidate other sessions for this user
            invalidate_other_sessions(user)
            
            auth_login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()    
    return render(request, 'registration/login.html', {'form': form})




# def logout(request):
#     logout(request)  # Log out the user
#     return JsonResponse({'success': True})