from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from EcoWorld.models import ongoingChallenge, dailyObjective, card

class Post(models.Model):
    """
    Model for storing forum posts.
    This includes challenge completions, daily objectives, and card achievements.
    """
    POST_TYPES = [
        ('challenge', 'Challenge Completion'),
        ('objective', 'Daily Objective'),
        ('card', 'Card Achievement'),
    ]

    VISIBILITY = [
        ('friends', 'Friends Only'),
        ('university', 'University Wide'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=20, choices=POST_TYPES)
    visibility = models.CharField(max_length=20, choices=VISIBILITY, default='university')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Reference to the actual content (only one should be non-null)
    challenge = models.ForeignKey(ongoingChallenge, on_delete=models.CASCADE, null=True, blank=True)
    objective = models.ForeignKey(dailyObjective, on_delete=models.CASCADE, null=True, blank=True)
    card_achievement = models.ForeignKey(card, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s {self.post_type} post"

class PostInteraction(models.Model):
    """
    Model for storing post interactions (likes/dislikes).
    """
    INTERACTION_TYPES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']  # A user can only have one interaction per post
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} {self.interaction_type}d {self.post}"
