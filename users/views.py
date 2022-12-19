from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from .token import account_activation_token  
from django.core.mail import EmailMessage  
from django.utils.encoding import force_bytes  
from django.utils.encoding import force_str as force_text
from django.contrib.auth.models import User

def send_email_confirmation(request, user):
    current_site = get_current_site(request)  
    mail_subject = 'Activation link has been sent to your email id'  
    message = render_to_string('users/acc_active_email.html', {  
        'user': user,  
        'domain': current_site.domain,  
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
        'token':account_activation_token.make_token(user),  
    })  
    to_email = user.email 
    email = EmailMessage(  
        mail_subject, message, to=[to_email]  
    )  
    email.send()

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account was created for {username}, to finish registration, check your {email} inbox to confirm your email')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_email_confirmation(request, user)
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

def activate(request, uidb64, token):   
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return render(request, 'users/email-confirm.html', {'success' : True})
    else:  
        return render(request, 'users/email-confirm.html', {'success' : False})