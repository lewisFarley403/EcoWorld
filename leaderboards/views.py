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
    return render(request, 'leaderboard/leaderboard.html')

# def get_ranked_users(request):
#     """
#     Function to return the top 10 users in the leaderboard
#     Returns:
#         (users,scores) : QuerySet,{User:Int} : users, a sorted list of user objects, scores, a dictionary of user objects to their scores
#     Author: Lewis Farley ()
#     """
#     users = User.objects.all()
#     coin_map = {}
#     for user in users:
#         coins_earnt = sum([i.score for i in UserEarntCoins.objects.filter(user=user)])
#         coin_map[user.username] = coins_earnt
#     users = sorted(coin_map, key=coin_map.get, reverse=True)
#     print(users)
#     print(coin_map)
#     # return as json
#     d ={'rankedUsers':users,'userPointMap':coin_map}
#     return JsonResponse(d)
@login_required
def get_ranked_users(request):
    """
    Returns the top 3 users in the leaderboard.
    Returns:
        JsonResponse: JSON response with ranked users and their respective scores
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
    for i in range(len(sorted_users)):
        user, score = sorted_users[i]
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
    username = request.GET.get("username", None)  # Default if no username is provided
    g = garden.objects.get(userID__username=username)
    squares = g.gardensquare_set.all()
    processedSquares = [[squares[i * g.size + j] for j in range(g.size)] for i in range(g.size)]

    user = request.user
    user = User.objects.get(id=user.id)
    # return render(request, 'Garden/garden.html', {'squares': processedSquares,
    #                                               'MEDIA_URL': settings.MEDIA_URL,
    #                                               'size': g.size,
    #                                               "userinfo": userinfo,
    #                                               "playerInventory": playerItems})
    return render(request, "leaderboard/garden_tool_tip.html", {"username": username,
                                                      "squares": processedSquares,
                                                      "MEDIA_URL": settings.MEDIA_URL,})
