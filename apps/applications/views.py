from rest_framework import viewsets
from .models import Application
from .serializers import ApplicationSerializer

from .permissions import IsApplicantOrJobOwner
from django.db.models import Q

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsApplicantOrJobOwner]

    def get_queryset(self):
        user = self.request.user
        qs = Application.objects.none()

        if "Applicant" in user.user_type or "Employer & Applicant" in user.user_type:
            qs = qs | Application.objects.filter(applicant=user)
        
        if "Employer" in user.user_type or "Employer & Applicant" in user.user_type:
            qs = qs | Application.objects.filter(job__company__owner=user)
        
        return qs.distinct()