# from django.shortcuts import render
# from django.http import HttpResponse

# # Create your views here.
# def home(request):
#     return HttpResponse("Hello world")


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Projects, ProjectMember
from .serializers import ProjectSerializer, ProjectDetailSerializer, ProjectMemberSerializer
from .permissions import IsProjectMember, IsProjectAdmin

User = get_user_model()

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Projects.objects.all()
        return Projects.objects.filter(members__user=user)

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMember.objects.create(project=project, user=self.request.user, role='admin')

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if request.user.role != 'admin' and project.owner != request.user:
            return Response({'error': 'Only owner or system admin can delete'}, status=403)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        project = get_object_or_404(Projects, pk=pk)
        self._check_access(request, project)
        members = project.members.select_related('user').all()
        return Response(ProjectMemberSerializer(members, many=True).data)

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        project = get_object_or_404(Projects, pk=pk)
        self._check_project_admin(request, project)
        user_id = request.data.get('user_id')
        role = request.data.get('role', 'member')
        user = get_object_or_404(User, id=user_id)
        member, created = ProjectMember.objects.get_or_create(
            project=project, user=user,
            defaults={'role': role}
        )
        if not created:
            return Response({'error': 'User already a member'}, status=409)
        return Response(ProjectMemberSerializer(member).data, status=201)

    @action(detail=True, methods=['delete'], url_path='remove_member/(?P<user_id>[^/.]+)')
    def remove_member(self, request, pk=None, user_id=None):
        project = get_object_or_404(Projects, pk=pk)
        self._check_project_admin(request, project)
        ProjectMember.objects.filter(project=project, user_id=user_id).delete()
        return Response({'message': 'Member removed'})

    def _check_access(self, request, project):
        if request.user.role == 'admin':
            return
        if not project.members.filter(user=request.user).exists():
            raise PermissionError('Not a member of this project')

    def _check_project_admin(self, request, project):
        if request.user.role == 'admin':
            return
        if not project.members.filter(user=request.user, role='admin').exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only project admins can manage members')