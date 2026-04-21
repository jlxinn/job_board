import django_filters 
from .models import Job

class JobFilters(django_filters.FilterSet):
    location = django_filters.CharFilter(lookup_expr='icontains')
    title = django_filters.CharFilter(lookup_expr='icontains')
    min_salary = django_filters.NumberFilter(field_name='salary', lookup_expr='gte')
    max_salary = django_filters.NumberFilter(field_name='salary', lookup_expr='lte')

    class Meta:
        model = Job
        fields = ['is_active']