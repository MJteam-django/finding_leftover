from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    restaurant = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post', default='default_image.jpg') #사용자에게 이미지 파일을 입력받아 화면에 띄우고 싶습니다.
    memo = models.TextField(blank=True)
    local = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    origin_price = models.IntegerField(default=0)
    new_price = models.IntegerField(default=0)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    #해당 User의 모든 posts를 모두 가져오고 싶을때 사용할 ORM은 post=user.post.all()
    soldout = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']

