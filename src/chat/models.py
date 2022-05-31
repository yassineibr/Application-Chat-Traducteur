from django.db import models
from django.contrib.auth.models import User
from googletrans import LANGUAGES

def get_User():
    return UserProfile.objects.get(id = 1)

# Create your models here.

class UserProfile(models.Model):
    """
        Model for User Profile
    """

    langChoice = [ (key, LANGUAGES[key].title()) for key in LANGUAGES.keys()]

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    languageKey = models.CharField(default="en", max_length = 10, choices=langChoice, verbose_name="Language")

    def __str__(self) -> str:
        return self.user.username


class PrivateMessages(models.Model):
    """
        Model for Private Messages inside a private room
    """
    chatroomname = models.CharField(max_length=30,null=True)
    sender = models.ForeignKey(UserProfile,default=1, on_delete=models.SET(get_User), related_name="sender")
    receiver = models.ForeignKey(UserProfile,default=1, on_delete=models.SET(get_User), related_name="receiver") 
    text = models.CharField(max_length = 10000)
    timestamp = models.DateTimeField(auto_now_add=True)

class TranslatedPrivateMessages(models.Model):
    """
        Model for Translated Private Messages
    """
    srcMessage = models.ForeignKey(PrivateMessages, on_delete=models.CASCADE)
    text = models.CharField(max_length = 10000)

# class ChatChannel(models.Model):
#     """
#     Model for Group Chats TODO
#     """
#     name = models.CharField(max_length=128)
#     createdBy = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
#     members = models.ManyToManyField(UserProfile)
#     timestamp = models.DateTimeField(auto_now_add=True)
