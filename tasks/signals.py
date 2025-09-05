from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, QuickAction

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()

@receiver(post_save, sender=UserProfile)
def create_default_quick_actions(sender, instance, created, **kwargs):
    """Create default quick actions for new user profiles."""
    if created:
        default_actions = [
            {
                'label': 'Add Task',
                'icon': 'fas fa-plus',
                'action_type': 'modal',
                'order': 1
            },
            {
                'label': 'Due Today',
                'icon': 'fas fa-clock',
                'action_type': 'filter',
                'action_data': {'filter_type': 'due_date', 'filter_value': 'today'},
                'order': 2
            },
            {
                'label': 'High Priority',
                'icon': 'fas fa-star',
                'action_type': 'filter',
                'action_data': {'filter_type': 'priority', 'filter_value': 'high'},
                'order': 3
            },
            {
                'label': 'Report',
                'icon': 'fas fa-chart-bar',
                'action_type': 'modal',
                'order': 4
            }
        ]
        
        for action_data in default_actions:
            QuickAction.objects.create(
                user=instance.user,
                **action_data
            )
