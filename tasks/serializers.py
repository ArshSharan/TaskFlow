from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, UserProfile, QuickAction

class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    profile_photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'display_name', 'bio', 'profile_photo', 'profile_photo_url', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_profile_photo_url(self, obj):
        if obj.profile_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_photo.url)
        return None

class QuickActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickAction
        fields = ['id', 'label', 'icon', 'action_type', 'action_data', 'order', 'is_active', 'created_at']
        read_only_fields = ['created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'category', 'due_date', 'created_at', 'updated_at', 'user']
        read_only_fields = ['user', 'created_at', 'updated_at'] 