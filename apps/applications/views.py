from rest_framework import viewsets
from .models import Application
from .serializers import ApplicationSerializer
from rest_framework.response import Response

from .permissions import IsApplicantOrJobOwner
from django.db.models import Q

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsApplicantOrJobOwner]

    def get_queryset(self):
        user = self.request.user

        return Application.objects.filter(
            Q(applicant=user) | Q(job__compnay__owner=user)
        ).distinct
    
    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        if "status" not in request.data:
            return Response({"error": "Можно менять только статус"}, status=400)
        
        return super().partial_update(request, *args, **kwargs)