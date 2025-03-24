"""
Models for the forum functionality.

This module defines the database models for forum-related features,
including posts and user interactions. The models support:
    - Multiple post types (challenges, objectives, cards, guides)
    - Visibility control (friends-only or university-wide)
    - Post interactions (likes/dislikes)
    - Automatic post creation from various sources
"""

from django.db import models
from django.contrib.auth.models import User
from EcoWorld.models import challenge, card

class Post(models.Model):
    """
    Model for storing and managing forum posts.

    This model handles different types of posts including challenge completions,
    daily objectives, card achievements, and guides. Posts can be configured
    for different visibility levels and contain various types of content.

    Attributes:
        user (ForeignKey): The user who created the post
        post_type (str): Type of post (challenge/objective/card/guide)
        visibility (str): Post visibility level (friends/university)
        created_at (DateTimeField): Timestamp of post creation
        challenge (ForeignKey): Optional linked challenge
        card_achievement (ForeignKey): Optional linked card
        title (str): Optional post title
        description (str): Optional post description
        submission (str): Optional challenge submission text
        score (int): Optional guide completion score
    Author:
        Lewis Farley (lf507@exeter.ac.uk)
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
        """
        Create a new post from a completed challenge.

        Args:
            ongoing_challenge (OngoingChallenge): The completed challenge to create a post from

        Returns:
            Post: The newly created post instance
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
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
        """
        Create a new post from a card achievement.

        Args:
            card_obj (Card): The card that was achieved
            user (User): The user who achieved the card

        Returns:
            Post: The newly created post instance
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
        post = Post(
            user=user,
            post_type='card',
            card_achievement=card_obj
        )
        post.save()
        return post

    @staticmethod
    def create_from_guide(title, description, user, score):
        """
        Create a new post from a completed guide.

        Args:
            title (str): The title of the guide
            description (str): Description of the guide completion
            user (User): The user who completed the guide
            score (int): The score achieved in the guide

        Returns:
            Post: The newly created post instance
        Author:
            Lewis Farley (lf507@exeter.ac.uk)
        """
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
    Model for managing user interactions with posts.

    Tracks likes and dislikes on posts, ensuring each user can only
    have one type of interaction per post.

    Attributes:
        user (ForeignKey): The user who interacted with the post
        post (ForeignKey): The post that was interacted with
        interaction_type (str): Type of interaction (like/dislike)
        created_at (DateTimeField): Timestamp of the interaction
    Author:
        Lewis Farley (lf507@exeter.ac.uk)
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
