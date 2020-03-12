from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    body=models.TextField(default='000000',editable=True)
    counts=models.IntegerField(default=1)
    topwords=models.TextField(default='000000',editable=True)

    def __str__(self):
        return self.body
