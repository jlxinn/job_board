from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsCompanyOwner
from .models import Company
from .serializers import CompanySerializer
from rest_framework.filters import SearchFilter

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOwner]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
