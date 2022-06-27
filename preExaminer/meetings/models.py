import datetime
from django.db import models
from datetime import time
# Create your models here.
class rollnumber(models.Model):
    rollno=models.BigIntegerField('Roll Number',blank=False)
    name=models.CharField(max_length=100,blank=True)
    branch=models.CharField(max_length=100,blank=True)