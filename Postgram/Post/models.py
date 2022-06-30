from email.policy import default
from operator import mod
from django.db import models
from django.contrib.auth import get_user_model
import uuid
import datetime

from django.forms import UUIDField

User=get_user_model()


# Create your models here.
class Profile(models.Model):
    Relationship_choices=[('None', 'None'),('Single','Single'),('In a relationship','In a relationship'),('Married','Married'),('Engaged','Engaged')]       
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user=models.IntegerField() 
    bio = models.TextField(blank=True)
    profileimage=models.ImageField(upload_to='profile_images',default='blank-profile-picture.png')
    location = models.CharField(max_length=120,blank=True)
    Relationship_status=models.CharField(max_length=20,choices=Relationship_choices,default='None')
    Workplace=models.TextField(blank=True)

    
    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.CharField(max_length=50)
    user_profileimage=models.ImageField(default='blank-profile-picture.png')
    image=models.ImageField(upload_to='post_images')
    caption=models.TextField()
    post_date=models.DateTimeField(default=datetime.datetime.now)
    likes=models.IntegerField(default=0)
    
    def __str__(self) :
        return self.user
    
class Likepost(models.Model):
    post_id=models.CharField(max_length=1000)
    username=models.CharField(max_length=50)
    
    def __str__(self) :
        return self.username
    
class Followers(models.Model):
    user=models.CharField(max_length=100)
    follower=models.CharField(max_length=100)
    
    def __str__(self) :
        return self.user
    
        
    
    
