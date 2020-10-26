from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer

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

class Postmethodprac(APIView):
    