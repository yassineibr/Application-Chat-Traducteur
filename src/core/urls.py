from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as users_views

urlpatterns = [
    path('chat/',include('chat.urls')),
    path('admin/', admin.site.urls),
    path('register/', users_views.register, name='register'),
    path('profile/', users_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # path('login/', users_views.login, name='login'),
]
