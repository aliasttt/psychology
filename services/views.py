from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Service, FAQ


class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(is_active=True)


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.get_object()
        context['faqs'] = FAQ.objects.filter(
            service=service,
            is_active=True
        )
        context['other_services'] = Service.objects.filter(
            is_active=True
        ).exclude(id=service.id)[:3]
        return context


def faq_list(request):
    faqs = FAQ.objects.filter(is_active=True, service__isnull=True)
    return render(request, 'services/faq_list.html', {'faqs': faqs})
