from django.db import models
from django.conf import settings

class Application(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")

    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("applicant", "job")

        indexes = [
            models.Index(fields=[ "job", "status"])
        ]