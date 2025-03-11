from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

@login_required
def play_game(request):
    return render(request, 'SustainabilityGame/game.html')

@login_required
def save_score(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        score = data.get('score')
        trash_collected = data.get('trashCollected')

        # Calculate coins earned
        coins_earned = round(trash_collected * (score / 20))

        # Get player profile and update number_of_coins
        profile = request.user.profile
        profile.number_of_coins += coins_earned
        profile.save()

        return JsonResponse({
            'status': 'success',
            'coins_earned': coins_earned
        })
    return JsonResponse({'status': 'error'})