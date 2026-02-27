from django.db import models
from django.contrib.auth.models import AbstractUser
from authemail.models import EmailUserManager, EmailAbstractUser

# Create your models here.


class MyUser(EmailAbstractUser):
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=80, blank=True)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        default='profile_images/default.jpg'
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS  = ['email',]

    objects = EmailUserManager()


