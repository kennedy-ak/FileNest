from django import forms
from .models import User
from django.contrib.auth.forms import SetPasswordForm as BaseSetPasswordForm

from django.contrib.auth.forms import PasswordResetForm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) # setting it as password


class SetPasswordForm(BaseSetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        strip=False,
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        fields = []

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
        return user
    
    
class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}),
    )