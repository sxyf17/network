from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return self.username

    def following(self):
        return self.followers.all()   
        
class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userPost')
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        formatted_date = self.created_at.strftime('%m-%d-%Y %I:%M %p')
        formatted_update = self.updated_at.strftime('%m-%d-%Y %I:%M %p')
        return f"{self.content}: {self.likes} by {self.user} at {formatted_date}, updated on {formatted_update}"
    
    def serialize(self):
        return {
            "content": self.content,
            "user": self.user.username,
            "likes": self.likes,
            "created_at": self.created_at.strftime('%m-%d-%Y %I:%M %p'),
            "updated_at": self.updated_at.strftime('%m-%d-%Y %I:%M %p')
        }   

    

    