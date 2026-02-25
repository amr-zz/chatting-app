from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class MyUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        default='profile_images/default.jpg'
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS  = ['email',]


