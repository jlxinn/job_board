from rest_framework import viewsets
from .models import Job
from .serializers import JobSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsCompanyOwner
from django.shortcuts import get_object_or_404
from apps.companies.models import Company
from .filters import JobFilters

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOwner]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobFilters
    search_fields = ['title', 'description', 'company__name']
    ordering_fields = ['salary', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        company_id = self.request.data.get('company')

        company = get_object_or_404(
            Company,
            id=company_id,
            owner=self.request.user
        )
        serializer.save(company=company)

    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get('is_active')

        if is_active is None:
            queryset = queryset.filter(is_active=True)

        return queryset