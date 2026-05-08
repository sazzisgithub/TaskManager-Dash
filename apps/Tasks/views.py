from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Q, Count
from .models import Task, TaskComment
from .serializers import TaskSerializer, TaskDetailSerializer, TaskCommentSerializer
from apps.Project.models import ProjectMember

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.select_related('assignee', 'creator', 'project')

        if user.role != 'admin':
            member_projects = ProjectMember.objects.filter(user=user).values_list('project_id', flat=True)
            qs = qs.filter(project_id__in=member_projects)

        # Filters
        project_id = self.request.query_params.get('project')
        if project_id:
            qs = qs.filter(project_id=project_id)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)

        assignee = self.request.query_params.get('assignee')
        if assignee == 'me':
            qs = qs.filter(assignee=user)
        elif assignee:
            qs = qs.filter(assignee_id=assignee)

        overdue = self.request.query_params.get('overdue')
        if overdue == 'true':
            qs = qs.filter(due_date__lt=timezone.now().date()).exclude(status='done')

        priority = self.request.query_params.get('priority')
        if priority:
            qs = qs.filter(priority=priority)

        return qs

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        user = request.user
        # Members can only update their own assigned tasks or if project admin
        if user.role != 'admin':
            is_project_admin = ProjectMember.objects.filter(
                project=task.project, user=user, role='admin'
            ).exists()
            if not is_project_admin and task.creator != user and task.assignee != user:
                return Response({'error': 'Permission denied'}, status=403)
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        task = self.get_object()
        text = request.data.get('comment', '').strip()
        if not text:
            return Response({'error': 'Comment cannot be empty'}, status=400)
        comment = TaskComment.objects.create(task=task, user=request.user, comment=text)
        return Response(TaskCommentSerializer(comment).data, status=201)

    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')
        valid = [s[0] for s in Task.STATUS_CHOICES]
        if new_status not in valid:
            return Response({'error': f'Invalid status. Choose from {valid}'}, status=400)
        task.status = new_status
        task.save()
        return Response(TaskSerializer(task).data)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        if user.role == 'admin':
            base_qs = Task.objects.all()
        else:
            member_projects = ProjectMember.objects.filter(user=user).values_list('project_id', flat=True)
            base_qs = Task.objects.filter(project_id__in=member_projects)

        my_tasks = base_qs.filter(assignee=user)

        stats = {
            'total_tasks': base_qs.count(),
            'todo': base_qs.filter(status='todo').count(),
            'in_progress': base_qs.filter(status='in_progress').count(),
            'review': base_qs.filter(status='review').count(),
            'done': base_qs.filter(status='done').count(),
            'overdue': base_qs.filter(due_date__lt=today).exclude(status='done').count(),
            'my_tasks': my_tasks.count(),
            'my_overdue': my_tasks.filter(due_date__lt=today).exclude(status='done').count(),
        }

        recent_tasks = base_qs.select_related('assignee', 'creator', 'project').order_by('-updated_at')[:10]
        overdue_tasks = base_qs.filter(due_date__lt=today).exclude(status='done').select_related('assignee', 'creator', 'project').order_by('due_date')[:10]
        my_task_list = my_tasks.exclude(status='done').select_related('assignee', 'creator', 'project').order_by('due_date')[:10]

        return Response({
            'stats': stats,
            'recent_tasks': TaskSerializer(recent_tasks, many=True).data,
            'overdue_tasks': TaskSerializer(overdue_tasks, many=True).data,
            'my_tasks': TaskSerializer(my_task_list, many=True).data,
        })