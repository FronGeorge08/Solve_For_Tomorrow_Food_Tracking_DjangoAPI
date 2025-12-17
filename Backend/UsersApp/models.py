from django.db import models

class User(models.Model):
    name=models.CharField(max_length=20,null=False,blank=False)
    username=models.CharField(max_length=20,null=False,blank=False)
    email=models.EmailField()
    password=models.CharField(max_length=30,null=False,blank=False)
    description=models.CharField(max_length=200,null=False,blank=False)
    image=models.CharField(max_length=1000)
    is_active=models.BooleanField()
    
