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
    
from django.contrib.auth.models import User

class File(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class FileDownload(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    download_count = models.PositiveIntegerField(default=0)
    email_sent_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.file.title} - Downloads: {self.download_count}, Emails Sent: {self.email_sent_count}"