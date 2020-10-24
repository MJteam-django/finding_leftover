from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status # rest 프레임워크의 제네릭 가져오기/ 제네릭뷰 사용할거니까
from rest_framework.exceptions import ValidationError #exceptions 가져오기
from rest_framework.response import Response # delete할 때 필요한 리스폰스 가져오기
# permissions 가져와서 권한있는 사용자 구분
from .models import Post
from .serializers import PostSerializer # PostSerializer 가져오기

# 제네릭 뷰 사용하는 이 부분은 http렌더링 관련해서 찾아봐야할듯
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all() # 쿼리셋 설정해줘야하고
    serializer_class = PostSerializer # 시리얼라이저 클래스 설정해줘야함

    # 권한있는지 확인하는 permission_class(로그아웃 상태로는 list볼 수 있지만 create는 불가능)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # create 이벤트를 만들 때마다 poster를 만들거야
        serializer.save(poster=self.request.user)
