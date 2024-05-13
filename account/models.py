from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)
    
    def str(self):
        return f'Profile for user {self.user.username}'