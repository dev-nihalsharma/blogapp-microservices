from django.db import models

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=100, null=True)
    likes = models.PositiveIntegerField(default=0)
    content = models.TextField(null=True)




class User(models.Model):
    pass