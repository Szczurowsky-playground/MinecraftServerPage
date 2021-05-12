from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=16)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    image = models.CharField(max_length=256)
    text = models.TextField(max_length=2555)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
