from django.db import models
from Main.models import User
from django.conf import settings


# Create your models here.

class Ticket(models.Model):
    title = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='User')
    handled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, related_name='Admin', null=True)
    problem = models.TextField(max_length=255)
    solved = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' [' + str(self.user) + ']'


class Response(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=255)

    def __str__(self):
        return str(self.ticket.title) + ' [' + str(self.user) + '] ' + str(self.id)
