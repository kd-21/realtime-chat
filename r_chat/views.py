from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.http import JsonResponse
from r_chat.forms import RoomForm
from .models import Room,Messages
from django.urls import reverse
# Create your views here.

@login_required(login_url="/accounts/login/")
def rooms(request):
    rooms=Room.objects.all()
    return render(request, "chat/rooms.html",{"rooms":rooms})


class RoomCreateView(CreateView):
    model = Room
    fields = ['name']  # Fields required for room creation
    template_name = 'chat/room_form.html'

    def form_valid(self, form):
        # Save the room (slug generation happens in the model's save method)
        room = form.save()

        # Handle AJAX request
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Return JSON response with room details, including the URL
            room_url = reverse('room', kwargs={'slug': room.slug})  # Construct the URL for the room
            
            return JsonResponse({
                "success": True,
                "room": {
                    "name": room.name,
                    "slug": room.slug,
                    "url": room_url,  # Send the complete URL for the room
                },
            })

        # For standard form submission, redirect to room list or other view
        return super().form_valid(form)
    

# @login_required(login_url="/accounts/login/")
# def room(request, slug):
#     room_name=Room.objects.get(slug=slug).name
#     messages=Messages.objects.filter(room=Room.objects.get(slug=slug))
    
#     return render(request, "chat/chat_room.html",{
#         "room_name":room_name,
#         "slug":slug,
#         'messages':messages
#         })


@login_required(login_url="/accounts/login/")
def room(request, slug):
    # Fetch the room once to avoid repeating queries
    room = get_object_or_404(Room, slug=slug)
    messages = Messages.objects.filter(room=room)
    
    return render(request, "chat/chat_room.html", {
        "room_name": room.name,
        "slug": slug,
        "messages": messages
    })
