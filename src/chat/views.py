from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

# Create your views here.

@login_required
def index(request):
    return render(request, 'chat/index.html',{})

@login_required
def room(request, room_name):
    return render(request, 'chatroom.html', {
        'room_name' : room_name,
    })

@login_required
def privateRoom(request, dest_id):
    try : 
        dest = UserProfile.objects.get(pk=int(dest_id))
        return render(request, 'privateChatroom.html', {
            'dest_id': dest_id,
            'dest_name' : dest.user.username,
        })
    except Exception as e:
        print(e)

