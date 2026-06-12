from rest_framework import viewsets, status
from .models import Application
from apps.pagination import CustomPagination
from .serializers import ApplicationSerializer, StatusSerializer
from rest_framework.response import Response

from .permissions import ApplicantPermissions
from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend
from .filters import ApplicationFilters
from rest_framework.filters import OrderingFilter

from rest_framework.decorators import action
from rest_framework.response import Response



class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [ApplicantPermissions]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ApplicationFilters
    pagination_class = CustomPagination
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        return Application.objects.filter(
            Q(applicant=user) | Q(job__company__owner=user)
        ).select_related('applicant', 'job__company').distinct()
    
    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        if "status" not in request.data:
            return Response({"error": "Можно менять только статус"}, status=400)
        
        return super().partial_update(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def my (self, request):
        qs = self.get_queryset().filter(applicant=request.user)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def incoming(self, request):
        qs = self.get_queryset().filter(job__company__owner=request.user)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['PATCH'], serializer_class=StatusSerializer)
    def status(self, request, pk=None):
        application = self.get_object()
    
        if application.job.company.owner != request.user:
            return Response(
                {"error": "Нет прав"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = StatusSerializer(
            application, 
            data={'status': request.data.get('status')}, 
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)