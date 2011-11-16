# Django
from django.db import models

class FortuneCookie(models.Model):

    text = models.CharField(max_length=255)
