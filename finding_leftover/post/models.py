from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    restaurant = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    #image = models.ImageField(default='media/default.jpg')
    memo = models.TextField(blank=True)
    local = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    soldout = models.BooleanField(default=False)
    origin_price = models.IntegerField(default=0)
    new_price = models.IntegerField(default=0)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']

#pull request시험
    
