from django.shortcuts import render
from .models import UserProfile

# Create your views here.

def index(request):
    return render(request, 'index.html',{})


def room(request, room_name):
    return render(request, 'chatroom.html', {
        'room_name' : room_name,
    })

def privateRoom(request, dest_id):
    try : 
        dest = UserProfile.objects.get(pk=int(dest_id))
        return render(request, 'privateChatroom.html', {
            'dest_id': dest_id,
            'dest_name' : dest.user.username,
        })
    except Exception as e:
        print(e)

