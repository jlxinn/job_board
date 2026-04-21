from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.jobs.views import JobViewSet
from apps.applications.views import ApplicationViewSet
from apps.companies.views import CompanyViewSet
from apps.users.views import RegisterView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register("jobs", JobViewSet, basename='jobs')
router.register("companies", CompanyViewSet, basename='companies')
router.register("applications", ApplicationViewSet, basename='applications')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('auth/login/', obtain_auth_token),
]