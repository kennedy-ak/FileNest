from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User,Profile
from .forms import LoginForm
from django.db import transaction
from django.contrib.auth import  authenticate, login,logout
# Create your views here.
def dashboard(request):
    return render(request, "account/dashboard.html")


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')



def user_login(request):
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
        
    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect('/')
    #     else:
    #         messages.info(request, 'Credentials Invalid')
    #         return redirect('login')     
        
    # else:
    #     return render(request, "account/login.html")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Passing the authenticated user object here
                return redirect('dashboard')
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('login')
    else:
        form = LoginForm()
                
    return render(request, "account/login.html", {'form': form})

def user_register(request):
    
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            
            else:
                new_user = User.objects.create(username=username,email=email)
                
                new_user.set_password(password)
                with transaction:
                    
                    new_user.save(commit = False)
                    new_user.is_active= False
                    activateEmail(request, user,email)
                    
                    
                    
                    
                    
                
                    #create user profil
                    Profile.objects.create(user=new_user)                
                
                return render(request,"account/register_done.html",{'new_user':new_user})
    
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')
    return render(request, "account/register.html")


def user_logout(request):
    logout(request)
    return redirect('login')
    