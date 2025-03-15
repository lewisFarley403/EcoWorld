from django.shortcuts import render
from django.http import JsonResponse
from EcoWorld.models import ongoingChallenge, dailyObjective
from Accounts.models import Friends
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

@login_required
def get_challenge_info(request):
    filter_type = request.GET.get('filter', 'my')
    
    if filter_type == 'my':
        # Get only the current user's completed challenges
        completed_challenges = ongoingChallenge.objects.filter(
            user=request.user,
            submitted_on__isnull=False
        ).select_related('challenge', 'user')

        completed_objectives = dailyObjective.objects.filter(
            user=request.user,
            completed=True
        ).select_related('user')

    elif filter_type == 'friends':
        # Get friends' IDs
        friends = Friends.objects.filter(
            Q(userID1=request.user) | Q(userID2=request.user)
        )
        
        # Check if user has any friends
        if not friends.exists():
            return JsonResponse({
                'has_no_friends': True,
                'ongoing_challenges': [],
                'daily_objectives': []
            })

        friend_ids = set()
        for friend in friends:
            if friend.userID1 == request.user:
                friend_ids.add(friend.userID2.id)
            else:
                friend_ids.add(friend.userID1.id)
        
        # Get friends' completed challenges
        completed_challenges = ongoingChallenge.objects.filter(
            user_id__in=friend_ids,
            submitted_on__isnull=False
        ).select_related('challenge', 'user')

        completed_objectives = dailyObjective.objects.filter(
            user_id__in=friend_ids,
            completed=True
        ).select_related('user')

    else:  # university
        # Get all completed challenges
        completed_challenges = ongoingChallenge.objects.filter(
            submitted_on__isnull=False
        ).select_related('challenge', 'user')

        completed_objectives = dailyObjective.objects.filter(
            completed=True
        ).select_related('user')

    # Format the data
    challenge_data = {
        'has_no_friends': False,  # Default value for non-friends filter
        'ongoing_challenges': [
            {
                'name': challenge.challenge.name,
                'description': challenge.challenge.description,
                'submitted_on': challenge.submitted_on.isoformat() if challenge.submitted_on else None,
                'submission': challenge.submission,
                'completion_count': challenge.completion_count,
                'username': challenge.user.username
            }
            for challenge in completed_challenges
        ],
        'daily_objectives': [
            {
                'name': objective.name,
                'progress': objective.progress,
                'goal': objective.goal,
                'date_created': objective.date_created.isoformat(),
                'submission': objective.submission,
                'coins_earned': objective.coins,
                'username': objective.user.username
            }
            for objective in completed_objectives
        ]
    }

    return JsonResponse(challenge_data)

@login_required
def feed(request):
    # Get user info for navbar
    user = request.user
    user = User.objects.get(id=user.id)
    pfp_url = user.profile.profile_picture
    pfp_url = "/media/pfps/" + pfp_url

    userinfo = {
        "username": user.username,
        "pfp_url": pfp_url,
        "coins": user.profile.number_of_coins
    }

    return render(request, 'feed/feed.html', {'userinfo': userinfo})
