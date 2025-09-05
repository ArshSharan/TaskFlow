from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UserProfileViewSet, QuickActionViewSet, task_list, update_user

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'profile', UserProfileViewSet, basename='userprofile')
router.register(r'quick-actions', QuickActionViewSet, basename='quickaction')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/update_user/', update_user, name='update_user'),
    path('tasks/', task_list, name='task_list'),
] 