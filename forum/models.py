from django.db import models
from django.contrib.auth.models import User
from ecoworld.models import challenge, card

class Post(models.Model):
    """
    Model for storing forum posts.
    This includes challenge completions, daily objectives, and card achievements.
    """
    POST_TYPES = [
        ('challenge', 'Challenge Completion'),
        ('objective', 'Daily Objective'),
        ('card', 'Card Achievement'),
        ('guide', 'Guide'),
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
    challenge = models.ForeignKey(challenge, on_delete=models.CASCADE, null=True, blank=True)
    card_achievement = models.ForeignKey(card, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    submission = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)  # For guide completion scores
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s {self.post_type} post"

    @staticmethod
    def create_from_ongoing_challenge(ongoing_challenge):
        """Create a new post from a challenge completion."""
        post = Post(
            user=ongoing_challenge.user,
            post_type='challenge',
            challenge=ongoing_challenge.challenge,
            submission=ongoing_challenge.submission
        )
        post.save()
        return post

    @staticmethod
    def create_from_card(card_obj, user):
        """Create a new post from a card achievement."""
        post = Post(
            user=user,
            post_type='card',
            card_achievement=card_obj
        )
        post.save()
        return post

    @staticmethod
    def create_from_guide(title, description, user, score):
        """Create a new post from a guide completion."""
        post = Post(
            user=user,
            post_type='guide',
            title=title,
            description=description,
            score=score
        )
        post.save()
        return post

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
