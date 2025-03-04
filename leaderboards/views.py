from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserEarntCoins
from django.contrib.auth.models import User
from django.http import JsonResponse
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

def get_ranked_users(request):
    """
    Returns the top 3 users in the leaderboard.
    Returns:
        JsonResponse: JSON response with ranked users and their respective scores
    """
    users = User.objects.all()
    coin_map = {}

    # Loop through all users and sum their earned coins
    for user in users:
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

    # Return the data as a JSON response
    return JsonResponse({'rankedUsers': ranked_users})