from django.db import models

# Create your models here.


class CloudTable(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=20,null=False)
    email=models.EmailField(max_length=100,default="user@cloud.com")
    mob=models.CharField(max_length=10, unique=True)
    profile_pic=models.URLField(default="empty")
