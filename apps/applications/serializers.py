from rest_framework import serializers
from .models import Application
from apps.jobs.models import Job
from apps.jobs.serializers import JobSerializer

class ApplicationSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    job_detail = JobSerializer(source='job', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant', 'cover_letter', 'resume', 'status', 'created_at']
        read_only_fields = ['applicant', 'status', 'created_at']

    def validate(self, data):
        user = self.context["request"].user
        job = data.get("job")

        if job.company.owner == user:
            raise serializers.ValidationError("Нельзя откликаться на свою вакансию")
        
        if Application.objects.filter(applicant=user, job=job).exists():
            raise serializers.ValidationError("Вы уже откликались")
        
        return data

    def validate_status(self, value):
        instance = self.instance

        if not instance:
            return value
    
        if instance.status != "pending":
            raise serializers.ValidationError("Статус уже финальный")
        
        return value