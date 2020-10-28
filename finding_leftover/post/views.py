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

# 포스팅 목록 및 새 포스팅 작성
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
        
# 식당 검색
class StoreListAPI(ListAPIView):
    serializer_class = StoreSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'store_list.html'

    def get(self, request):
        # 검색을 아직하지않은 첫화면일때는 모든 store보여준다.
        queryset = Store.objects.all()
        storename = request.query_params.get('searchword', None)
        # 검색을 했을때는 queryset을 필터링해준다.
        if storename is not None:
            queryset = queryset.filter(store_name__icontains=storename)
        return Response({'stores': queryset})

# 식당의 상세 페이지
class StoreDetailAPIView(APIView):
    serializer_class = StoreSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'store_detail.html'

    def get(self, request, pk):
        store = Store.objects.get(pk=pk)
        user = User.objects.get(pk=pk)
        post = user.post.all()
        return Response({'store': store, 'posts':post})



# 판매글 작성
class PostCreateAPIView(CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'posting.html'

    def get(self, request): # get요청시 판매글 작성 폼 보여주기
        serializer = PostSerializer()
        return Response({'serializer': serializer})

    def post(self, request): # post요청시 판매글을 저장하고 post-list로 가게함
        serializer = PostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save(poster=self.request.user) 
        # perform_create()가 serializer.save()를 해줌
        return redirect('post-list') 

    """ 이 코드가 왜 안되는질 모르겠음ㅜㅜ
    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)
        redirect('post-list')
    """  
# 판매글의 update와 delete 요청
class PostUpdateAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_update.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response({'serializer': serializer, 'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'post': post})
        serializer.save()
        return redirect('post-list')

    def delete(self, request, pk, format=None): #특정 포스팅 삭제
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
