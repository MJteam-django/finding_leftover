from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status # rest 프레임워크의 제네릭 가져오기/ 제네릭뷰 사용할거니까
from rest_framework.exceptions import ValidationError #exceptions 가져오기
from rest_framework.response import Response # delete할 때 필요한 리스폰스 가져오기
# permissions 가져와서 권한있는 사용자 구분
from .models import Post
from .serializers import PostSerializer # PostSerializer 가져오기

# rendering html
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

# 제네릭 뷰 사용하는 이 부분은 http렌더링 관련해서 찾아봐야할듯
class PostList(APIView):
    queryset = Post.objects.all() # 쿼리셋 설정해줘야하고
    serializer_class = PostSerializer # 시리얼라이저 클래스 설정해줘야함

    # html rendering
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_list.html'

    # 권한있는지 확인하는 permission_class(로그아웃 상태로는 list볼 수 있지만 create는 불가능)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # create 이벤트를 만들 때마다 poster를 만들거야
        serializer.save(poster=self.request.user)
    
    def get(self, request):
        queryset = Post.objects.all()
        return Response({'posts': queryset})

class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all() # 쿼리셋 설정해줘야하고
    serializer_class = PostSerializer # 시리얼라이저 클래스 설정해줘야함

    # 권한있는지 확인하는 permission_class(로그아웃 상태로는 list볼 수 있지만 create는 불가능)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 로그인한 사용자가 post 게시자와 다르면 삭제하지 못하게 하는 메서드
    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('This isn\'t your post to delete!')