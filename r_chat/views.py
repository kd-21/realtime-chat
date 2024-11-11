from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Room,Messages
# Create your views here.

@login_required(login_url="/accounts/login/")
def rooms(request):
    rooms=Room.objects.all()
    return render(request, "chat/rooms.html",{"rooms":rooms})



@login_required(login_url="/accounts/login/")
def room(request,slug):
    room_name=Room.objects.get(slug=slug).name
    messages=Messages.objects.filter(room=Room.objects.get(slug=slug))
    
    return render(request, "chat/chat_room.html",{"room_name":room_name,"slug":slug,'messages':messages})