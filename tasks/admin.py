from django.contrib import admin
from .models import Task, UserProfile, QuickAction

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'category', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'created_at')
    search_fields = ('user__username', 'user__email', 'display_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(QuickAction)
class QuickActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'label', 'icon', 'action_type', 'order', 'is_active')
    list_filter = ('action_type', 'is_active', 'created_at')
    search_fields = ('user__username', 'label')
    readonly_fields = ('created_at',)
    ordering = ('user', 'order')
