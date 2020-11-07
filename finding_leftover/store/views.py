from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from store.models import Store
from post.serializers import PostSerializer
from store.serializers import StoreSerializer
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import User 
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from post.pagination import CustomPagination
from django.http import HttpResponse
import json

# 식당 이름으로 검색
class StorenameListAPI(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'store_name_list.html'
    pagination_class = CustomPagination

    def get(self, request):
        # 검색을 아직하지않은 첫화면일때는 모든 store보여준다.
        queryset = Store.objects.all()
        storename = request.query_params.get('searchword', None)
        
        # 검색을 했을때는 queryset을 필터링해준다.
        if storename is not None:
            queryset = queryset.filter(store_name__icontains=storename)
        
        # page_size만큼의 post만 보내도록 queryset 재설정
        self.paginator.page_size_query_param = "page_size"
        page = self.paginate_queryset(queryset)
        
        if page is not None: 
            mypage = self.paginator.get_html_context() # page에 관련된 정보
            return Response({'stores' : page, 'mypage' : mypage })

        return Response({'stores': queryset})

# 식당 지역으로 검색
class StorelocalListAPI(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'store_local_list.html'
    pagination_class = CustomPagination


    def get(self, request):
        # 검색을 아직하지않은 첫화면일때는 모든 store보여준다.
        queryset = Store.objects.all()
        local = request.query_params.get('searchword', None)

        # 검색을 했을때는 queryset을 필터링해준다.
        if local is not None:
            queryset = queryset.filter(store_local__icontains=local)
        
        # page_size만큼의 post만 보내도록 queryset 재설정
        self.paginator.page_size_query_param = "page_size"
        page = self.paginate_queryset(queryset)
        
        if page is not None: 
            mypage = self.paginator.get_html_context() # page에 관련된 정보
            return Response({'stores' : page, 'mypage' : mypage, 'local':local })

        return Response({'stores': queryset, 'local':local})

# 식당의 상세 페이지 조회
class StoreDetailAPIView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'store_detail.html'
    pagination_class = CustomPagination


    def get(self, request, pk):
        store = Store.objects.get(pk=pk)
        user = User.objects.get(pk=pk)
        queryset = user.post.all()

        # 6 만큼의 post만 보내도록 queryset 재설정
        self.paginator.page_size = 6
        page = self.paginate_queryset(queryset)

        if page is not None: 
            mypage = self.paginator.get_html_context() # page에 관련된 정보
            return Response({'store': store, 'posts':page, 'mypage' : mypage})

        return Response({'store': store, 'posts':queryset})
    
    # 식당의 좋아요에 관한 요청(ajax POST요청으로 들어옴)
    def post(self, request, pk):
        store = get_object_or_404(Store, pk=pk)
        user = request.user

        if store.store_like_user.filter(id=user.id).exists():
            store.store_like_user.remove(user)
            msg = "좋아요 취소"
        else:
            store.store_like_user.add(user)
            msg = "좋아요"
        
        count = store.count_likes_user()
        store.store_like_count = count
        store.save()
        context = {'like_count':store.count_likes_user(), 'msg':msg}
        return HttpResponse(json.dumps(context), content_type="application/json")
        

         


