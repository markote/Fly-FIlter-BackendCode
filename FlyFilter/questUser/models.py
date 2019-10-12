from __future__ import unicode_literals

from django.db import models
class respuestasUser(models.Model):

    class Meta:
        app_label = 'questUser'

    idResp = models.CharField(max_length=20,primary_key=True)
    resp = models.TextField()
# Create your models here.
