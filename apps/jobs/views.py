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

from rest_framework.decorators import action
from rest_framework.response import Response

from apps.pagination import CustomPagination


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOwner]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobFilters
    pagination_class = CustomPagination

    search_fields = ['title', 'description', 'company__name']
    ordering_fields = ['salary', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get('is_active')

        if is_active is None:
            queryset = queryset.filter(is_active=True)

        return queryset
    
    @action(detail=False, methods=['get'])
    def my(self, request):
        qs = self.get_queryset().filter(company__owner=request.user)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)