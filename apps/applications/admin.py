from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicantionAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'created_at']
    list_filter = ['created_at',]
    search_fields = ['applicant', 'job']
    readonly_fields = ['created_at']

    fieldsets = (
        # Группировка полей в админке
        ('Основная инфомрация', {
            'fields': ('job', 'applicant')
        }),
        ('Временные метки', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )