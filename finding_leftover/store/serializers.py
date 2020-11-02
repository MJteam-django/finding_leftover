from rest_framework import serializers
from post.models import Store 

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__' #지금은 그냥 all로 했는데 필요시 추가수정