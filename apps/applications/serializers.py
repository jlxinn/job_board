from rest_framework import serializers
from .models import Application
from jobs.serializers import JobSerializer

class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant', 'cover_letter', 'resume', 'status', 'created_at']
        read_only_fields = ['applicant', 'status', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        job = self.context['job']

        application = Application.objects.create(applicant=user, job=job, **validated_data)

        return application