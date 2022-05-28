from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm,UserProfileRegistrationForm, UserUpdateForm, ProfileUpdateForm
from chat.models import UserProfile

# Create your views here.


def register(request):
    if request.method == "POST":
        u_form = UserRegistrationForm(request.POST)
        p_form = UserProfileRegistrationForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            new_user = u_form.save()
            new_userprofile = UserProfile.objects.create(
                user=new_user,
                languageKey=p_form.cleaned_data['languageKey']
            )
            new_userprofile.save()
            messages.success(request, f'Your account has been created! You are now able to log in ')
            return redirect('login')

    else :
        u_form = UserRegistrationForm()
        p_form = UserProfileRegistrationForm()
    return render(request, "users/register.html", {
        'u_form' : u_form,
        'p_form' : p_form,
    })

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account has been updated')
            return redirect('profile')

    else : 
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'u_form': u_form, 
        'p_form': p_form, 
    }
    return render(request, 'users/profile.html', context)