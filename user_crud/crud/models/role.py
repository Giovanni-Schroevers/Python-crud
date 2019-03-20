from django.db import models


class Role(models.Model):
    ident = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return 'Role: {}'.format(self.ident)
