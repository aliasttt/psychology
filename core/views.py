from django.shortcuts import render
from django.views.generic import TemplateView
from services.models import Service
from blog.models import Post


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)[:6]
        context['recent_posts'] = Post.objects.filter(is_published=True)[:3]
        return context


def privacy_policy(request):
    return render(request, 'core/privacy.html')


def cookie_policy(request):
    return render(request, 'core/cookies.html')
