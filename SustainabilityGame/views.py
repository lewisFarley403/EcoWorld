from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import GameSession, Achievement, UserAchievement
import json

@login_required
def game_home(request):
    # Get user's previous games and achievements
    user_games = GameSession.objects.filter(user=request.user).order_by('-date_played')[:5]
    user_achievements = UserAchievement.objects.filter(user=request.user)

    context = {
        'user_games': user_games,
        'user_achievements': user_achievements,
    }
    return render(request, 'SustainabilityGame/home.html', context)


@login_required
def play_game(request):
    return render(request, 'SustainabilityGame/game.html')


@login_required
def save_score(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            score = data.get('score', 0)

            # Save game session with just the score
            game = GameSession.objects.create(
                user=request.user,
                score=score
            )

            # Award coins based on score (e.g., 1 coin per 10 points)
            coins_earned = score // 10
            if coins_earned > 0:
                request.user.profile.coins += coins_earned
                request.user.profile.save()

            # Check for achievements
            # Example: Award an achievement for first game played
            if GameSession.objects.filter(user=request.user).count() == 1:
                first_game_achievement = Achievement.objects.filter(name="First Game").first()
                if first_game_achievement and not UserAchievement.objects.filter(user=request.user, achievement=first_game_achievement).exists():
                    UserAchievement.objects.create(user=request.user, achievement=first_game_achievement)

            # Example: Award an achievement for high score
            if score >= 100:
                high_score_achievement = Achievement.objects.filter(name="High Score").first()
                if high_score_achievement and not UserAchievement.objects.filter(user=request.user, achievement=high_score_achievement).exists():
                    UserAchievement.objects.create(user=request.user, achievement=high_score_achievement)

            return JsonResponse({'status': 'success', 'coins_earned': coins_earned})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error'})


@login_required
def leaderboard(request):
    top_scores = GameSession.objects.order_by('-score')[:20]
    return render(request, 'SustainabilityGame/leaderboard.html', {'top_scores': top_scores})