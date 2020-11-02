from django.views.generic.base import TemplateView

#해당 템플릿을 렌더링하는 제네릭뷰
class HomeView(TemplateView):
    template_name = 'home.html'