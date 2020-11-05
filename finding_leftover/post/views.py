from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from post.models import Post
from store.models import Store
from post.serializers import PostSerializer
from store.serializers import StoreSerializer
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import User 
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
import simplejson as json #ajax
from django.http import HttpResponse
from rest_framework import status
from post.pagination import CustomPagination

# 포스팅 지역으로 검색
class PostListAPIView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_list.html'
    pagination_class = CustomPagination

    def get(self, request):
        # 검색을 아직하지않은 첫화면일때는 모든 post를 작성시간순으로 보여준다.
        queryset = Post.objects.all()
        local = request.query_params.get('searchword', None)
        
        # 검색을 했을때는 queryset을 필터링해준다.
        if local is not None:
            queryset = queryset.filter(local__icontains=local)

        # page_size만큼의 post만 보내도록 queryset 재설정
        self.paginator.page_size_query_param = "page_size"
        page = self.paginate_queryset(queryset)
        
        if page is not None: 
            mypage = self.paginator.get_html_context() # page에 관련된 정보
            return Response({'posts' : page, 'mypage' : mypage, 'local':local })
        return Response({'posts': queryset, 'local':local})

# 포스팅 제목으로 검색
class PostSearchListAPIView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_search_list.html'
    pagination_class = CustomPagination

    def get(self, request):
        # 검색을 아직하지않은 첫화면일때는 모든 post를 작성시간순으로 보여준다.
        queryset = Post.objects.all()
        title = request.query_params.get('searchword', None)
        
        # 검색을 했을때는 queryset을 필터링해준다.
        if title is not None:
            queryset = queryset.filter(title__icontains=title)

        # page_size만큼의 post만 보내도록 queryset 재설정
        self.paginator.page_size_query_param = "page_size"
        page = self.paginate_queryset(queryset)
        
        if page is not None: 
            mypage = self.paginator.get_html_context() # page에 관련된 정보
            return Response({'posts' : page, 'mypage' : mypage, 'title':title })
        return Response({'posts': queryset, 'title':title})

# 포스팅 상세 조회
class PostDetailAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_detail.html'

    def get(self, request, pk):
        queryset = Post.objects.get(pk=pk)
        discount = int((queryset.origin_price-queryset.new_price)/ queryset.origin_price *100) # 할인율
        return Response({'post': queryset, 'discount':discount})
        

# 포스팅 작성
class PostCreateAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_create.html'

    # 포스팅 작성 폼 보여주기
    def get(self, request): 
        # form클래스 대신 serializer
        serializer = PostSerializer()
        return Response({'serializer': serializer})

    # 작성한 포스팅을 저장하고 전체 포스팅 목록으로
    def post(self, request): 
        serializer = PostSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'serializer': serializer})
        
        user=self.request.user 
        # post와 유저를 연결, post에관한 유저정보는 사용자가 입력하는 것이아닌 자동으로
        serializer.save(poster=user,restaurant=user.store.store_name,local=user.store.store_local) 
        # perform_create()가 serializer.save()를 해줌
        return redirect('post-list') 


# 포스팅의 수정과 삭제
class PostUpdateAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_update.html'

    # 포스팅 수정 폼 보여주기
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        # form클래스 대신 serializer
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