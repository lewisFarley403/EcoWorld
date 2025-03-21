import json

from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q, Count, Case, When, IntegerField
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from Accounts.models import Friends
from EcoWorld.models import ongoingChallenge, card
from EcoWorld.views import getUserInfo
from .models import Post, PostInteraction


# Create your views here.

@login_required
def get_challenge_info(request):
    filter_type = request.GET.get('filter', 'my')
    user = request.user

    # Base queryset for posts
    posts = Post.objects.select_related(
        'user', 'user__profile',
        'challenge', 'card_achievement'
    )

    if filter_type == 'my':
        # Get user's posts
        posts = posts.filter(user=user)
        
    elif filter_type == 'friends':
        # Get friends list
        friends = Friends.objects.filter(
            Q(userID1=user) | Q(userID2=user)
        )
        
        if not friends.exists():
            return JsonResponse({
                'has_no_friends': True,
                'ongoing_challenges': [],
                'card_achievements': [],
                'guides': []
            })

        friend_ids = []
        for friend in friends:
            if friend.userID1 == user:
                friend_ids.append(friend.userID2.id)
            else:
                friend_ids.append(friend.userID1.id)

        # Get friends' posts
        posts = posts.filter(user_id__in=friend_ids)

    # Format the data with only the fields needed by the template
    challenge_data = {
        'has_no_friends': False,  # Default value for non-friends filter
        'ongoing_challenges': [
            {
                'id': post.id,
                'name': post.challenge.name,
                'description': post.challenge.description,
                'submission': post.submission if hasattr(post, 'submission') else None,
                'completion_count': post.challenge.completion_count if hasattr(post.challenge, 'completion_count') else 1,
                'submitted_on': post.created_at.isoformat(),
                'username': post.user.username,
                'redirect_url': post.challenge.redirect_url if hasattr(post.challenge, 'redirect_url') else None
            }
            for post in posts.filter(post_type='challenge')
        ],
        'card_achievements': [
            {
                'id': post.id,
                'name': post.card_achievement.title,
                'description': post.card_achievement.description,
                'rarity': post.card_achievement.rarity.title,
                'image': post.card_achievement.image.url if post.card_achievement.image else None,
                'username': post.user.username,
                'created_at': post.created_at.isoformat()
            }
            for post in posts.filter(post_type='card')
        ],
        'guides': [
            {
                'id': post.id,
                'title': post.title,
                'description': post.description,
                'score': post.score,
                'username': post.user.username,
                'created_at': post.created_at.isoformat()
            }
            for post in posts.filter(post_type='guide')
        ],
        'daily_objectives': []  # Empty list since we don't have daily objectives in the backend yet
    }

    return JsonResponse(challenge_data)

@login_required
def feed(request):
    return render(request, 'feed/feed.html', {'username': request.user.username})

@login_required
def create_post(request):
    """Create a new post for a challenge completion, daily objective, or card achievement."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        post_type = data.get('post_type')
        content_id = data.get('content_id')
        visibility = data.get('visibility', 'university')

        # Validate post type
        if post_type not in ['challenge', 'objective', 'card']:
            return JsonResponse({"error": "Invalid post type"}, status=400)

        # Create post based on type
        post_data = {
            'user': request.user,
            'post_type': post_type,
            'visibility': visibility
        }

        if post_type == 'challenge':
            challenge = ongoingChallenge.objects.get(id=content_id, user=request.user)
            post_data['challenge'] = challenge

        elif post_type == 'card':
            card_obj = card.objects.get(id=content_id)
            post_data['card_achievement'] = card_obj

        post = Post.objects.create(**post_data)
        return JsonResponse({"success": True, "post_id": post.id})


    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@login_required
def interact_with_post(request):
    """Handle post likes and dislikes."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        post_id = data.get('post_id')
        interaction_type = data.get('type')

        if interaction_type not in ['like', 'dislike']:
            return JsonResponse({"error": "Invalid interaction type"}, status=400)

        post = Post.objects.get(id=post_id)
        interaction, created = PostInteraction.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={'interaction_type': interaction_type}
        )

        if not created:
            if interaction.interaction_type == interaction_type:
                # Remove the interaction if clicking the same button
                interaction.delete()
                action = "removed"
            else:
                # Change the interaction type if clicking a different button
                interaction.interaction_type = interaction_type
                interaction.save()
                action = "changed"
        else:
            action = "added"

        # Get updated counts
        likes = post.interactions.filter(interaction_type='like').count()
        dislikes = post.interactions.filter(interaction_type='dislike').count()

        return JsonResponse({
            "success": True,
            "action": action,
            "likes": likes,
            "dislikes": dislikes
        })

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@login_required
def get_post_interactions(request, post_id):
    """Get the current like/dislike counts for a post."""
    try:
        post = Post.objects.get(id=post_id)
        user_interaction = post.interactions.filter(user=request.user).first()
        
        return JsonResponse({
            "likes": post.interactions.filter(interaction_type='like').count(),
            "dislikes": post.interactions.filter(interaction_type='dislike').count(),
            "user_interaction": user_interaction.interaction_type if user_interaction else None
        })
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

@permission_required("Accounts.can_view_gamekeeper_button")
def delete_post(request, post_id):
    """Delete a post and its interactions."""
    print('deleting post')
    if request.method == "POST":
        print('deleting post')
        print(post_id)
        post = get_object_or_404(Post, id=post_id)
        print('post : ',post)
        post.delete()
        print('post deleted')
        # post.save()
        print('post saved')
        return redirect('forum:forum_gamekeeper')
    else:
        print('not a post')
        return redirect('forum:forum_gamekeeper')

@permission_required("Accounts.can_view_gamekeeper_button")
def forum_gamekeeper(request):
    """
    View for the forum gamekeeper page that allows gamekeepers to manage forum posts.
    Shows all posts with their interaction statistics and allows deletion of posts.
    
    Author:
        Lewis Farley (lf507@exeter.ac.uk)
    """
    # Get all posts ordered by creation date
    posts = Post.objects.all().order_by('-created_at')
    posts_data = []
    
    for post in posts:
        likes = PostInteraction.objects.filter(post=post, interaction_type='like').count()
        dislikes = PostInteraction.objects.filter(post=post, interaction_type='dislike').count()
        ratio = f"{dislikes/(likes + dislikes):.2%}" if (likes + dislikes) > 0 else "N/A"
        posts_data.append({
            'post': post,
            'likes': likes,
            'dislikes': dislikes,
            'ratio': ratio
        })
    
    return render(request, 'forum/forum_gamekeeper.html', {
        'posts': posts_data
    })
