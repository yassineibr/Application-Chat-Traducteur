from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('@groups/<str:room_name>/', views.room, name='room'),
    path('@me/<str:dest_id>/', views.privateRoom, name='private_room'),
    path('@me/', views.prvRooms, name='prv_rooms'),
]