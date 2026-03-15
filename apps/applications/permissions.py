from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsApplicantOrJobOwner(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False
        
        if request.method == "POST":
            return "Applicant" in user.user_type or "Regular User" in user.user_type
        
        if request.method in SAFE_METHODS:
            return "Appplicant" in user.user_type or "Employer" in user.user_type or "Employer & Applicant" in user.user_type
        return True
    
    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in SAFE_METHODS:

            if "Appplicant" in user.user_type or "Employer & Applicant" in user.user_type:
                if obj.applicant == user:
                    return True
                
            if "Employer" in user.user_type or "Employer & Applicant" in user.user_type:
                if obj.job.company.owner == user:
                    return True
            return False
        
        if request.method in ["PATCH", "PUT"]:
            if obj.applicant == user:
                return True
            if obj.job.company.owner == user:
                return True
            return False
        
        if request.method == "DELETE":
            if obj.applicant == user:
                return True
            return False
        
        return False