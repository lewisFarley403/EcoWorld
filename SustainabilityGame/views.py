import json
import math

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

@login_required
def play_game(request):
    """Render the sustainability game page
    Requires user authentication

    Author:
        sg916@exeter.ac.uk
    """
    return render(request, 'SustainabilityGame/game.html')

@login_required
def save_score(request):
    """Save game score and award coins to user
    - Processes POST request with game score
    - Calculates coins earned based on score
    - Updates user's profile with new coins
    - Returns success/error status and coins earned

    Requires user authentication

    Author:
        sg916@exeter.ac.uk
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        score = data.get('score')

        # Calculate coins earned from score
        coins_earned = calculate_coins(score)

        # Update user's coin balance
        profile = request.user.profile
        profile.number_of_coins += coins_earned
        profile.save()

        return JsonResponse({
            'status': 'success',
            'coins_earned': coins_earned
        })
    return JsonResponse({'status': 'error'})

def calculate_coins(score):
    """Calculate coins earned from game score
    - No coins earned for scores below 150
    - Exponential reward scaling using formula: 4 * e^(0.005 * (score - 150))

    Args:
        score (int): Player's game score
    Returns:
        int: Number of coins earned

    Author:
        sg916@exeter.ac.uk
    """
    if score < 150:
        return 0
    a = 4  # Base reward multiplier
    b = 0.005  # Exponential growth rate
    return round(a * math.exp(b * (score - 150)))
