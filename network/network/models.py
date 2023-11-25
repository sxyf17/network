from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", related_name='usersFollowing', blank=True)
    following = models.ManyToManyField("self", related_name='userFollowers', blank=True)
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": [follower.username for follower in self.followers.all()],
            "following": [followed.username for followed in self.following.all()]
        }   
class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userPost')
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        formatted_date = self.created_at.strftime('%m-%d-%Y %I:%M %p')
        return f"{self.content}: {self.likes} by {self.user} at {formatted_date}"

    

    