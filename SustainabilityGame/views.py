
import json
import math

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


@login_required
def play_game(request):
    return render(request, 'SustainabilityGame/game.html')

@login_required
def save_score(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        score = data.get('score')

        # Calculate coins earned
        coins_earned = calculate_coins(score)

        # Get player profile and update number_of_coins
        profile = request.user.profile
        profile.number_of_coins += coins_earned
        profile.save()

        return JsonResponse({
            'status': 'success',
            'coins_earned': coins_earned
        })
    return JsonResponse({'status': 'error'})

def calculate_coins(score):
    if score < 150:
        return 0
    a = 4
    b = 0.005
    return round(a * math.exp(b * (score - 150)))