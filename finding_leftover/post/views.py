from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Post, Store
from .serializers import PostSerializer, StoreSerializer
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import User 

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
        discount = int(100 / (queryset.origin_price / queryset.new_price))
        return Response({'post': queryset, 'discount':discount})

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

class StoreDetailAPIView(APIView):
    serializer_class = StoreSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'store_detail.html'

    def get(self, request, pk):
        store = Store.objects.get(pk=pk)
        user = User.objects.get(pk=pk)
        post = user.post.all()
        return Response({'store': store, 'posts':post})
