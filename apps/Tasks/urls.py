from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, DashboardView

router = DefaultRouter()
router.register('', TaskViewSet, basename='task')

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', include(router.urls)),
]

