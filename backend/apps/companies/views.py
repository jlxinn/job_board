from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import CompaniesPermissions
from .models import Company
from .serializers import CompanySerializer
from rest_framework.filters import SearchFilter
from apps.pagination import CustomPagination

from rest_framework.decorators import action
from rest_framework.response import Response

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, CompaniesPermissions]
    filter_backends = [SearchFilter]
    pagination_class = CustomPagination
    search_fields = ['name', 'description']
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def my(self, request):
        qs = self.get_queryset().filter(owner=request.user)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)