"""
Views for the leaderboard functionality.

This module contains view functions for handling leaderboard-related requests,
including displaying the leaderboard page, retrieving ranked user data, and
generating garden tooltips for user profiles. It provides functionality for:
    - Rendering the main leaderboard page
    - Calculating and returning user rankings based on earned coins
    - Displaying garden information in tooltips

All views in this module require user authentication except where noted.

Author:
    Lewis Farley (lf507@exeter.ac.uk)
"""

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from Garden.models import garden
from .models import UserEarntCoins


# Create your views here.
@login_required
def leaderboard(request):
    """
    Render the leaderboard page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered leaderboard template.

    Author:
        Lewis Farley (lf507@exeter.ac.uk)
    """
    return render(request, 'leaderboard/leaderboard.html')

@login_required
def get_ranked_users(request):
    """
    Get the ranked users for the leaderboard.

    Calculates and returns user rankings based on their earned coins,
    excluding admin users. Also includes the current user's rank and score.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON object containing:
            - rankedUsers: List of dictionaries with user data 
                            (username, profile picture URL, score)
            - MEDIA_URL: The media URL from settings
            - current_user_data: Dictionary with current user's username, score, and rank

    Author:
        Lewis Farley (lf507@exeter.ac.uk)
    """
    current_user = request.user
    users = User.objects.all()
    coin_map = {}

    # Loop through all users and sum their earned coins
    for user in users:
        if not user.username == "admin":
                coins_earnt = sum([i.score for i in UserEarntCoins.objects.filter(user=user)])
                coin_map[user] = coins_earnt  # Map user to their total score

    # Sort the users based on their earned coins in descending order
    sorted_users = sorted(coin_map.items(), key=lambda x: x[1], reverse=True)

    # Prepare data for the top 3 users
    ranked_users = []
    for i,(user,score) in enumerate(sorted_users):
        ranked_users.append({
            'username': user.username,
            'pfp_url': "/media/pfps/" +user.profile.profile_picture,
            'score': score
        })
    for i,u in enumerate(ranked_users):
        if u['username'] == current_user.username:
            current_user_rank = i+1
            break
    current_user_data = {
        'username': current_user.username,
        'score': coin_map[current_user],
        'rank': current_user_rank
    }
    # Return the data as a JSON response
    return JsonResponse({'rankedUsers': ranked_users,'MEDIA_URL': settings.MEDIA_URL,'current_user_data':current_user_data})


def get_tooltip_template(request):
    """
    Get the garden tooltip template for a specific user.

    Retrieves and processes garden data for the specified user to display
    in a tooltip overlay.

    Args:
        request: The HTTP request object containing a 'username' GET parameter.

    Returns:
        HttpResponse: The rendered garden tooltip template with context including:
            - username: The requested user's username
            - squares: 2D list of processed garden squares
            - MEDIA_URL: The media URL from settings

    Author:
        Lewis Farley (lf507@exeter.ac.uk)
    """
    username = request.GET.get("username", None)  # Default if no username is provided
    g = garden.objects.get(userID__username=username)
    squares = g.gardensquare_set.all()
    processed_squares = [[squares[i * g.size + j] for j in range(g.size)] for i in range(g.size)]
    user = request.user
    user = User.objects.get(id=user.id)
    return render(request, "leaderboard/garden_tool_tip.html", {"username": username,
                                                      "squares": processed_squares,
                                                      "MEDIA_URL": settings.MEDIA_URL,})
