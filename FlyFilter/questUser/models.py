from __future__ import unicode_literals

from django.db import models
class respuestasUser(models.Model):
    idResp = models.CharField(max_length=20,primary_key=True)
    resp = models.TextField()
# Create your models here.
