from rest_framework import viewsets
from .models import Job
from .serializers import JobSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsCompanyOwner
from django.shortcuts import get_object_or_404
from apps.companies.models import Company

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOwner]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['location', 'salary']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        company_id = self.request.data.get('company')

        company = get_object_or_404(
            Company,
            id=company_id,
            owners=self.request.user
        )
        serializer.save(company=company)