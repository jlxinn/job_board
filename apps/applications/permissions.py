from rest_framework.permissions import BasePermission, SAFE_METHODS

class ApplicantPermissions(BasePermission):

    def has_permission(self, request, view):
        if not request.user  or not request.user.is_authenticated:
            return False
        
        if request.method == 'POST':
            return True 
        return True
    
    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in SAFE_METHODS:
            return (
                obj.applicant == user or obj.job.company.owner == user 
            )
        
        if request.method in ["PATCH", "PUT"]:
            return obj.job.company.owner == user
        
        if request.method == "DELETE":
            return obj.applicant == user
        
        return False