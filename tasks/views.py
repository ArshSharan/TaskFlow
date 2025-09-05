from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
import json
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Task, UserProfile, QuickAction
from .serializers import TaskSerializer, UserProfileSerializer, QuickActionSerializer

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """Get dashboard statistics for the current user"""
        user = request.user
        today = timezone.now().date()
        
        # Task counts
        total_tasks = Task.objects.filter(user=user).count()
        completed_tasks = Task.objects.filter(user=user, status='completed').count()
        in_progress_tasks = Task.objects.filter(user=user, status='in_progress').count()
        overdue_tasks = Task.objects.filter(
            user=user, 
            due_date__lt=today, 
            status__in=['pending', 'in_progress']
        ).count()
        
        # Calculate productivity percentage
        productivity = round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0)
        
        # Tasks by priority
        high_priority = Task.objects.filter(user=user, priority='high', status__in=['pending', 'in_progress']).count()
        
        # Recent tasks (last 7 days)
        week_ago = today - timedelta(days=7)
        recent_completed = Task.objects.filter(
            user=user, 
            status='completed', 
            updated_at__date__gte=week_ago
        ).count()
        
        return Response({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'overdue_tasks': overdue_tasks,
            'productivity': productivity,
            'high_priority_tasks': high_priority,
            'recent_completed': recent_completed
        })

    @action(detail=False, methods=['get'])
    def filter_tasks(self, request):
        """Filter tasks based on various criteria"""
        filter_type = request.query_params.get('filter_type')
        filter_value = request.query_params.get('filter_value')
        
        queryset = self.get_queryset()
        
        if filter_type == 'due_date':
            today = timezone.now().date()
            if filter_value == 'today':
                queryset = queryset.filter(due_date=today)
            elif filter_value == 'overdue':
                queryset = queryset.filter(due_date__lt=today, status__in=['pending', 'in_progress'])
            elif filter_value == 'this_week':
                week_end = today + timedelta(days=7)
                queryset = queryset.filter(due_date__range=[today, week_end])
        
        elif filter_type == 'priority':
            queryset = queryset.filter(priority=filter_value)
        
        elif filter_type == 'status':
            queryset = queryset.filter(status=filter_value)
        
        elif filter_type == 'category':
            queryset = queryset.filter(category=filter_value)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        profile = self.get_object()
        serializer = self.get_serializer(profile, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update_profile(self, request):
        """Update current user's profile"""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password"""
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if not current_password or not new_password:
            return Response({'error': 'Both current and new passwords are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if len(new_password) < 8:
            return Response({'error': 'New password must be at least 8 characters long'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password changed successfully'})

class QuickActionViewSet(viewsets.ModelViewSet):
    serializer_class = QuickActionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QuickAction.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def reorder(self, request):
        """Reorder quick actions"""
        action_orders = request.data.get('actions', [])
        
        for item in action_orders:
            try:
                action = QuickAction.objects.get(
                    id=item['id'], 
                    user=request.user
                )
                action.order = item['order']
                action.save()
            except QuickAction.DoesNotExist:
                continue
        
        return Response({'status': 'success'})

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple quick actions at once"""
        actions_data = request.data.get('actions', [])
        created_actions = []
        
        for action_data in actions_data:
            action_data['user'] = request.user.id
            serializer = self.get_serializer(data=action_data)
            if serializer.is_valid():
                action = serializer.save(user=request.user)
                created_actions.append(serializer.data)
        
        return Response({'actions': created_actions, 'count': len(created_actions)})

@login_required
def task_list(request):
    return render(request, 'tasks/task_list.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to find user by email
        try:
            username = User.objects.get(email=email).username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'tasks/auth.html', {'is_login': True})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'tasks/auth.html', {'is_login': False})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'tasks/auth.html', {'is_login': False})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'tasks/auth.html', {'is_login': False})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'tasks/auth.html', {'is_login': False})

def logout_view(request):
    logout(request)
    return redirect('login')

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    """Update user information (email, first_name, last_name)"""
    user = request.user
    
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    
    if email and email != user.email:
        # Check if email is already taken
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user.email = email
    
    if first_name is not None:
        user.first_name = first_name
    
    if last_name is not None:
        user.last_name = last_name
    
    user.save()
    
    return Response({
        'message': 'User updated successfully',
        'user': {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }
    })
