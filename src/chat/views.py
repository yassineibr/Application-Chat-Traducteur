from django.http.response import Http404
from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from .models import UserProfile, PrivateMessages, TranslatedPrivateMessages

# Create your views here.

@login_required
def index(request):
    return render(request, 'chat/index.html',{})

@login_required
def room(request, room_name):
    return render(request, 'chat/groupChat.html', {
        'room_name' : room_name,
    })

@login_required
def prvRooms(request):
    try : 
        users = UserProfile.objects.all()[1:]
            
        return render(request, 'chat/prvChatrooms.html', {
            'user_profiles' : users,
        })
    except Exception as e:
        raise Http404("User not found")

@login_required
def privateRoom(request, dest_id):
    try : 
        dest = UserProfile.objects.get(pk=int(dest_id))
        user = request.user.userprofile

        if  user.id > int(dest.id):
            room_name = f"prvchat_{user.id}_{dest.id}"
        else:
            room_name = f"prvchat_{dest.id}_{user.id}"

        msgs = list(PrivateMessages.objects.filter(chatroomname = room_name))
        if user.languageKey != dest.languageKey:
            for i in range(len(msgs)):
                if msgs[i].sender.languageKey != user.languageKey:
                    try:
                        transMsg = TranslatedPrivateMessages.objects.get(srcMessage = msgs[i])
                        msgs[i].text = transMsg.text
                    except Exception as e:
                        print(e)
        
        users = UserProfile.objects.all()[1:]
            
        return render(request, 'chat/privateChatroom.html', {
            'dest_id': dest_id,
            'dest_name' : dest.user.username,
            'chat_messages' : msgs,
            'user_profiles' : users,
        })
    except Exception as e:
        print(e)

