from django.db.models.signals import post_save  
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User


#user와 Store을 연결시켜 user모델확장
#하나의 user은 하나의 store을 가진다.
class Store(models.Model):  
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,related_name='store')
    #해당 User가 모든 store를 가지고 오고 싶을 사용할 이름 store=user.store.all()
    store_name = models.CharField(max_length=50, blank=True)
    store_address = models.CharField(max_length=50, blank=True)
    store_image = models.ImageField(upload_to='store', default='default_image.jpg')
    store_memo = models.TextField(null=True, blank=True)
    store_like = models.IntegerField(null=True, blank=True)
    store_local = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        ordering = ['-store_name']

# User가 생성될때 같이 Profile도 만들어라
@receiver(post_save, sender=User)
def create_Store(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_store = Store(user=user)
        user_store.save()