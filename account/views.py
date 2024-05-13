from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User,Profile
from .forms import LoginForm
from django.db import transaction
from django.contrib.auth import  authenticate, login,logout

from django.template.loader import  render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage


from .tokens import account_activation_token
# Create your views here.
def dashboard(request):
    return render(request, "account/dashboard.html")



def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("account/template_activate.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, 'verfify account')
        # f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
        #         received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def activate(request,uidb64,token):
    return render(request,'account/home.html')

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Check if the user is active and the account has been saved
                if user.is_active:
                    login(request, user)  # Passing the authenticated user object here
                    return redirect('dashboard')
                else:
                    messages.info(request, 'Your account is not activated yet.')
                    return redirect('login')
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('login')
    else:
        form = LoginForm()
                
    return render(request, "account/login.html", {'form': form})

def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                try:
                    with transaction.atomic():
                        new_user = User.objects.create(username=username, email=email, is_active=False)
                        new_user.set_password(password)
                        # Activate email
                        activateEmail(request, new_user, email)
                        # Save user changes
                        new_user.save()
                        # Create user profile
                        profile = Profile.objects.create(user=new_user)
                        # Set is_active to True after email activation
                        new_user.is_active = True
                        new_user.save()
                    return render(request, "account/register_done.html", {'new_user': new_user})
                except Exception as e:
                    messages.error(request, f"Error: {e}")
                    return redirect('register')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')
    return render(request, "account/register.html")

def user_logout(request):
    logout(request)
    return redirect('login')
    