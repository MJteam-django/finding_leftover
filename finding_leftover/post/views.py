from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Post, Store
from .serializers import PostSerializer, StoreSerializer
from rest_framework.filters import SearchFilter

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
        return Response({'post': queryset})


class StoreListAPI(ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'store_list.html'

#    filter_backends = [SearchFilter]
#    search_fields = ['store_name']

    def get(self, request):
        queryset = Store.objects.all()
        return Response({'stores': queryset})
        

class SearchStoreList(ListAPIView):
    serializer_class = StoreSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'store_searched_list.html'

    def get_queryset(self):
        name = self.kwargs['storename']
        return Store.objects.filter(store_name=name) 
    def get(self, request, storename):
        name = self.kwargs['storename']
        queryset = Store.objects.filter(store_name=name) 
 #       queryset = Store.objects.all()
        return Response({'stores': queryset,'name':name})        