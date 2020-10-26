from django.contrib import admin
from .models import Post, Store # 모델 만든거 가져오기
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User 


#StackedInline : User과 profile이 연결되어 세로로 나열되게 해서 같이 저장하게끔
class StoreInline(admin.StackedInline):  
    model = Store
    can_delete = False

class NewUserAdmin(UserAdmin):  
    inlines = [StoreInline, ]


admin.site.unregister(User)  #기존의 자동으로 register되던 User는 취소시키고
admin.site.register(User, NewUserAdmin) #user받을때 Store도 같이 받는다.
admin.site.register(Post)