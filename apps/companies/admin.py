from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['owner', 'name', 'website', 'created_at']
    list_filter = ['owner', 'created_at']
    search_fields = ['name', 'owner']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'website')
        }),
        ('Временные метки',{
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )