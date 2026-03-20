from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsApplicantOrJobOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return (
                obj.applicant == request.user or obj.job.company.owner == request.user
            )
        
        if request.method in ["PATCH", "PUT"]:
            return obj.job.company.owner == request.user
        
        if request.method == "DELETE":
            return obj.applicant == request.user
        
        return False