import django_filters
from .models import Application

class ApplicationFilters(django_filters.FilterSet):
    status = django_filters.CharFilter()


    class Meta:
        model = Application
        fields = []