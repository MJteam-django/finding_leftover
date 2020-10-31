from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .models import Post, Store
from .serializers import PostSerializer, StoreSerializer
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import User 
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
import simplejson as json #ajax
from django.http import HttpResponse
from rest_framework import status

# 포스팅 목록
class PostListAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_list.html'

    def get(self, request):
        queryset = Post.objects.all()
        return Response({'posts': queryset})

class PostDetailAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_detail.html'

    def get(self, request, pk):
        queryset = Post.objects.get(pk=pk)
        discount = int((queryset.origin_price-queryset.new_price)/ queryset.origin_price *100)
        return Response({'post': queryset, 'discount':discount})
        




# 포스팅 작성
class PostCreateAPIView(CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_create.html'

    # 포스팅 작성 폼 보여주기
    def get(self, request): 
        serializer = PostSerializer()
        return Response({'serializer': serializer})

    # 작성한 포스팅을 저장하고 전체 포스팅 목록으로
    def post(self, request): 
        serializer = PostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        user=self.request.user
        serializer.save(poster=user,restaurant=user.store.store_name,local=user.store.store_address) 
        # perform_create()가 serializer.save()를 해줌
        return redirect('post-list') 


# 포스팅의 수정과 삭제
class PostUpdateAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_update.html'

    # 포스팅 수정 폼 보여주기
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response({'serializer': serializer, 'post': post})

    # 포스팅을 수정하고 해당 식당 페이지로 이동해서 확인
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'post': post})
        serializer.save()
        return redirect('store-detail',post.poster.id) 

    # 포스팅 삭제
    def delete(self, request, pk, format=None): 
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return HttpResponse(json.dumps({'pk': pk}), content_type="application/json") 