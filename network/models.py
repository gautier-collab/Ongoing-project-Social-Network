import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followers = models.ManyToManyField("self", blank = True, related_name = "followedPages")

    def __str__(self):
        return f"{self.username} (email: {self.email})"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "posts")
    likes = models.ManyToManyField(User, blank = True, related_name = "likes", default=None)
    text = models.CharField(max_length=512)
    timestamp = models.IntegerField()

    def date(self):
        return datetime.datetime.fromtimestamp(self.timestamp).strftime('%B %d, %Y at %H:%M')

    def __str__(self):
        return f'Post #{self.id}. {self.user.username} wrote "{self.text}" on {self.date()}. This post has received {len(self.likes.all())} like(s).'
