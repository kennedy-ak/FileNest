from django.shortcuts import render,redirect
from django.contrib import messages
from django.template.loader import render_to_string
from .models import User,Profile,File,FileDownload
from django.utils.html import strip_tags
from django.db.models import Q
from .forms import LoginForm,SetPasswordForm,PasswordResetForm,AdminLoginForm,FileUploadForm,EmailFileForm
from django.db import transaction
from django.contrib.auth import  authenticate, login,logout
from django.contrib.auth.decorators import  login_required, user_passes_test
from django.template.loader import  render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import  urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView ,PasswordResetConfirmView,    PasswordResetCompleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import mimetypes

from django.conf import settings
import os

# Create your views here.



def is_admin(user):
    return user.is_staff


def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and is_admin(user):
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials or you are not an admin.')
    else:
        form = AdminLoginForm()
    return render(request, 'account/admin_login.html', {'form': form})


@login_required(login_url=settings.ADMIN_LOGIN_URL)
@user_passes_test(is_admin)
def admin_dashboard(request):
    
    return render(request, 'account/admin_dashboard.html')



@login_required(login_url=settings.ADMIN_LOGIN_URL)
@user_passes_test(is_admin)
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.uploaded_by = request.user
            file.save()
            FileDownload.objects.create(file=file)
            messages.success(request, 'File uploaded successfully.')
            return redirect('admin_dashboard')
    else:
        form = FileUploadForm()
    return render(request, 'account/upload_files.html', {'form': form})


@login_required(login_url=settings.ADMIN_LOGIN_URL)
@user_passes_test(is_admin)
def file_statistics(request):
    files = FileDownload.objects.all()
    return render(request, 'account/file_stats.html', {'files': files})


def homepage(request):
    return render(request, "account/homepage.html")


@login_required(login_url='login')
def dashboard(request):
    query = request.GET.get('q') 
    files = File.objects.all()
    if query:  # If a search query is provided
        files = files.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, "account/dashboard.html",{'files': files})


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
        messages.success(request, 'Account Verified')
    
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def activate(request,uidb64,token):
    return render(request,'account/home.html')


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('dashboard')
                    else:
                        messages.info(request, 'Your account is not activated yet.')
                        return redirect('login')
                else:
                    messages.info(request, 'Invalid Credentials')
                    return redirect('login')
            except User.DoesNotExist:
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


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')

    
@login_required(login_url='login')
def change_password_done(request):
    return render(request,'account/password_change_done.html')  


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()

            return redirect('password_changed')
    else:
        form = SetPasswordForm(user=request.user)
    return render(request, 'account/change_password.html', {'form': form})


def password_reset(request):
    form = PasswordResetForm()
    return render(request,'account/password_reset.html',{'form':form})


def passwordResetConfirm(request,uidb64,token):
    return redirect('login')


# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'account/password_reset.html'
#     form_class = PasswordResetForm
#     success_url = reverse_lazy('password_reset_done')
class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                # User with the entered email exists, proceed with sending the password reset email
                return self.form_valid(form)
            else:
                # User with the entered email does not exist
                form.add_error('email', 'No user with this email address exists.')
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'
    

@login_required(login_url='login')
def download_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    file_path = file.file.path
    file_name = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)

    # Increment download count
    file_download, created = FileDownload.objects.get_or_create(file=file)
    file_download.download_count += 1
    file_download.save()

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    
    
def send_file_via_email(request, file_id):
    file = get_object_or_404(File, id=file_id)
    
    if request.method == 'POST':
        form = EmailFileForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            subject = f"File: {file.title}"
            message = render_to_string('account/email_template.html', {'file': file, 'user': request.user})
            plain_message = strip_tags(message)
            email = EmailMessage(subject, plain_message, to=[recipient_email])
            email.attach_file(file.file.path)
            
            if email.send():
                file_download, created = FileDownload.objects.get_or_create(file=file)
                file_download.email_sent_count += 1
                file_download.save()
                messages.success(request, 'File sent successfully.')
            else:
                messages.error(request, 'Failed to send the file.')
            return redirect('dashboard')
    else:
        form = EmailFileForm()
    
    return render(request, 'account/send_file.html', {'form': form, 'file': file})




@login_required(login_url=settings.ADMIN_LOGIN_URL)
@user_passes_test(is_admin)
def edit_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES, instance=file)
        if form.is_valid():
            form.save()
            messages.success(request, 'File updated successfully.')
            return redirect('admin_dashboard')
    else:
        form = FileUploadForm(instance=file)
    return render(request, 'account/edit_file.html', {'form': form, 'file': file})

@login_required(login_url=settings.ADMIN_LOGIN_URL)
@user_passes_test(is_admin)
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    if request.method == 'POST':
        file.delete()
        messages.success(request, 'File deleted successfully.')
        return redirect('admin_dashboard')
    return render(request, 'account/delete_file.html', {'file': file})