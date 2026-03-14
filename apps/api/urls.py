from rest_framework.routers import DefaultRouter
from apps.jobs.views import JobViewSet
from apps.applications.views import ApplicationViewSet
from apps.companies.views import CompanyViewSets

router = DefaultRouter()
router.register("jobs", JobViewSet, basename='jobs')
router.register("companies", CompanyViewSets, basename='companies')
router.register("applications", ApplicationViewSet, basename='applications')

urlpatterns = router.urls