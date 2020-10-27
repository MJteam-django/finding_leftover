from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save  
from django.dispatch import receiver

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
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    #해당 User의 모든 posts를 모두 가져오고 싶을때 사용할 ORM은 post=user.post.all()

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created']

#user와 Store을 연결시켜 user모델확장
#하나의 user은 하나의 store을 가진다.
class Store(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True) 
    store_name = models.CharField(max_length=500, blank=True)
    store_adress = models.CharField(max_length=30, blank=True)
    #sotre_image = models.ImageField(default='media/default.jpg')
    store_memo = models.TextField(null=True, blank=True)

#User가 생성될때 같이 Profile도 만들어라
@receiver(post_save, sender=User)
def create_Store(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_store = Store(user=user)
        user_store.save()
