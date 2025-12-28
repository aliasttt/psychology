from django.contrib import admin
from .models import Service, FAQ


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'display_order', 'price', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FAQInline]
    fieldsets = (
        ('Content', {
            'fields': ('name', 'slug', 'short_description', 'full_description', 'image')
        }),
        ('Pricing & Details', {
            'fields': ('price', 'duration', 'display_order')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'service', 'is_active', 'display_order']
    list_filter = ['service', 'is_active']
    search_fields = ['question', 'answer']
