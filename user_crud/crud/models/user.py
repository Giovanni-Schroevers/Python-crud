from django.db import models
from .role import Role


class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Role, models.SET_NULL, null=True)
    banned = models.BooleanField(default=False)

    def __str__(self):
        return 'User: {}'.format(self.firstname)
