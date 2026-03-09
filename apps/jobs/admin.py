from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['company', 'title', 'description', 'salary', 'is_active']
    list_filter = ['company', 'title', 'salary', 'is_active']
    search_fields = ['company', 'title']
    readonly_fields = ['created_at']
    
    fieldsets = (
        # Группировка полей в админке
        ('Основная инфомрация', {
            'fields': ('company', 'title', 'description', 'salary')
        }),
        ('Временные метки', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
)