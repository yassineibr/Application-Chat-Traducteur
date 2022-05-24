from django.contrib import admin

from .models import UserProfile, PrivateMessages, TranslatedPrivateMessages 

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(PrivateMessages)
admin.site.register(TranslatedPrivateMessages)