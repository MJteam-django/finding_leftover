from rest_framework import serializers
# 시리얼라이저 가져오고
from .models import Store # Post 모델 가져오기

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__' #지금은 그냥 all로 했는데 필요시 추가수정