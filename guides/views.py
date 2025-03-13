from idlelib.rpc import request_queue

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required

from .forms import GuidesForm
from .models import ContentQuizPair, UserQuizResult, User
import json
from django.core.serializers.json import DjangoJSONEncoder

@permission_required("Accounts.can_view_admin_button")
def add_guide(request):
    if request.method == 'POST':
        form = GuidesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("EcoWorld:admin_page")

    else:
        form = GuidesForm()
    return render(request, "guides/add_guide.html", {'form':form})

@login_required
def menu_view(request):
    pairs = ContentQuizPair.objects.all()
    completed_pairs = UserQuizResult.objects.filter(user=request.user, is_completed=True).values_list(
        'content_quiz_pair_id', flat=True)

    user = request.user
    user = User.objects.get(id=user.id)
    pfp_url = user.profile.profile_picture
    pfp_url = "/media/pfps/" + pfp_url

    userinfo = []
    userinfo.append({
        "username": user.username,
        "pfp_url": pfp_url,
        "coins": user.profile.number_of_coins
    })

    pairs_with_status = []
    for pair in pairs:
        is_completed = pair.id in completed_pairs
        pairs_with_status.append({
            'pair': pair,
            'is_completed': is_completed
        })

    return render(request, 'guides/menu.html', {
        'pairs_with_status': pairs_with_status,
        'userinfo':userinfo[0]
    })

@login_required
def content_view(request, pair_id):
    pair = get_object_or_404(ContentQuizPair, id=pair_id)
    user = request.user
    user = User.objects.get(id=user.id)
    pfp_url = user.profile.profile_picture
    pfp_url = "/media/pfps/" + pfp_url

    userinfo = []
    userinfo.append({
        "username": user.username,
        "pfp_url": pfp_url,
        "coins": user.profile.number_of_coins
    })
    return render(request, 'guides/content.html', {
        'pair': pair,
        'userinfo':userinfo[0]
    })

@login_required
def quiz_view(request, pair_id):
    pair = get_object_or_404(ContentQuizPair, id=pair_id)

    user = request.user
    user = User.objects.get(id=user.id)
    pfp_url = user.profile.profile_picture
    pfp_url = "/media/pfps/" + pfp_url

    userinfo = []
    userinfo.append({
        "username": user.username,
        "pfp_url": pfp_url,
        "coins": user.profile.number_of_coins
    })
    if pair.quiz_questions:
        try:
            quiz_questions_json = json.dumps(pair.quiz_questions, cls=DjangoJSONEncoder)
        except TypeError:
            quiz_questions_json = "[]"
    else:
        quiz_questions_json = "[]"

    return render(request, 'guides/quiz.html', {
        'pair': pair,
        'quiz_questions_json': quiz_questions_json,
        'userinfo': userinfo[0]
    })

@login_required
def registerScore_view(request, pair_id):
    data = json.loads(request.body)
    score = int(data['score'])
    user = request.user
    pair = get_object_or_404(ContentQuizPair, id=pair_id)
    coins_reward = pair.reward

    try:
        result = UserQuizResult.objects.get(user=user, content_quiz_pair=pair)
    except UserQuizResult.DoesNotExist:
        result = UserQuizResult(user=user, content_quiz_pair=pair, best_result=0, previous_best=0, score=0)

    result.previous_best = result.best_result
    result.score = score
    if score > result.best_result:
        result.best_result = score
    print(pair.quiz_max_marks)
    print(result.previous_best)
    print(score)
    if result.previous_best < pair.quiz_max_marks and score == pair.quiz_max_marks:
        user = User.objects.get(id=user.id)
        user.profile.number_of_coins += coins_reward
        user.save()

    result.save()

    return JsonResponse({'status': 'success', 'redirect_url': f'/guides/results/{pair_id}/'})

@login_required
def results_view(request, pair_id):
    pair = get_object_or_404(ContentQuizPair, id=pair_id)
    result = UserQuizResult.objects.filter(user=request.user, content_quiz_pair=pair).first()

    user = request.user
    user = User.objects.get(id=user.id)
    pfp_url = user.profile.profile_picture
    pfp_url = "/media/pfps/" + pfp_url

    userinfo = []
    userinfo.append({
        "username": user.username,
        "pfp_url": pfp_url,
        "coins": user.profile.number_of_coins
    })

    return render(request, 'guides/results.html', {
        'score': result.score,
        'previous': result.previous_best,
        'best': result.best_result,
        'max':pair.quiz_max_marks,
        'userinfo': userinfo[0],
        'pair': pair
    })