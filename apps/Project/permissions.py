from rest_framework.permissions import BasePermission
from .models import ProjectMember

class IsProjectMember(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'admin':
            return True
        project_id = view.kwargs.get('pk') or view.kwargs.get('project_id')
        if not project_id:
            return True
        return ProjectMember.objects.filter(project_id=project_id, user=request.user).exists()

class IsProjectAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'admin':
            return True
        project_id = view.kwargs.get('pk') or view.kwargs.get('project_id')
        if not project_id:
            return False
        return ProjectMember.objects.filter(
            project_id=project_id, user=request.user, role='admin'
        ).exists()