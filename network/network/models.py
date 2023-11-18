from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userPost')
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        formatted_date = self.created_at.strftime('%m-%d-%Y %I:%M %p')  # Change the format as needed
        return f"{self.content}: {self.likes} by {self.user} at {formatted_date}"

    

    