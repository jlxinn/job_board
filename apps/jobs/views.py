from rest_framework import viewsets
from .models import Job
from .serializers import JobSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsCompanyOwner

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCompanyOwner]

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

    