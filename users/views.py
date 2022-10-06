from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {username}')
            form.save(commit=True)
            return redirect('home')
        else:
            messages.warning(request, 'Something went wrong, please try again')
        
    else:
        form = RegistrationForm()
    context = {
        'form' : form
    }
    return render(request, 'users/register.html', context)

@login_required
def profile_settings(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile-settings')
        else:
            messages.warning(request, 'Invalid Data, try again')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)
    context={
        'p_form' : p_form,
        'u_form' : u_form
    }
    return render(request, 'users/profile-settings.html', context)