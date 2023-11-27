from django.contrib.auth.models import User
from django.db import models
class Chatbox(models.Model):
    sp_id = models.IntegerField()
    farmer_id =models.IntegerField()
    senderid = models.IntegerField()
    recid = models.IntegerField()
    text=models.CharField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True)
