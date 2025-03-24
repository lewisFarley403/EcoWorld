"""
Views for the guides functionality.

This module contains view functions for handling guide-related requests,
including content management, quiz functionality, and score tracking. The views support:
    - Guide content creation and removal
    - Quiz management and scoring
    - User progress tracking
    - Markdown content rendering
    - Admin moderation features
"""

import json
import markdown

from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe

from forum.models import Post
from .forms import GuidesForm, DeleteForm
from .models import ContentQuizPair, UserQuizResult, User


@permission_required("Accounts.can_view_gamekeeper_button")
def remove_guide(request):
    """
    This view allows an admin to remove a content-quiz pair.

    Attributes:
        request (HttpRequest): The request object containing form data.

    Returns:
        HttpResponse: Redirects to the admin page after deleting the
        content-quiz pair.

    author:
        Johnny Say (js1687@exeter.ac.uk)
    """
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            selected_pair_id = form.cleaned_data['pair'].id
            pair = ContentQuizPair.objects.get(id=selected_pair_id)
            pair.delete()
            return redirect('EcoWorld:gamekeeper_page')
    else:
        form = DeleteForm()

    return render(request,"guides/remove_guide.html", {"form":form} )

@permission_required("Accounts.can_view_gamekeeper_button")
def add_guide(request):
    """
    This view allows an admin to add a new content-quiz pair.
    The content field supports Markdown formatting which will be rendered
    in the content view.

    Attributes:
        request (HttpRequest): The request object containing form data.

    Returns:
        HttpResponse: Redirects to the admin page after saving the new
            content-quiz pair.

    author:
        Johnny Say (js1687@exeter.ac.uk)
    """
    if request.method == 'POST':
        form = GuidesForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            questions = []
            max_marks = 0
            for key, value in request.POST.items():
                if key.startswith('question_'):
                    max_marks += 1
                    question_id = key.split('_')[1]
                    question = value
                    answers = [
                        {
                            "text": request.POST[f'answer1_{question_id}'],
                            "value": "A",
                            "correct": f'1' in request.POST.getlist(f'correct_answers_{question_id}')
                        },
                        {
                            "text": request.POST[f'answer2_{question_id}'],
                            "value": "B",
                            "correct": f'2' in request.POST.getlist(f'correct_answers_{question_id}')
                        },
                        {
                            "text": request.POST[f'answer3_{question_id}'],
                            "value": "C",
                            "correct": f'3' in request.POST.getlist(f'correct_answers_{question_id}')
                        },
                        {
                            "text": request.POST[f'answer4_{question_id}'],
                            "value": "D",
                            "correct": f'4' in request.POST.getlist(f'correct_answers_{question_id}')
                        }
                    ]
                    questions.append({
                        "question": question,
                        "answers": answers
                    })

            quiz_json = json.dumps(questions)

            pair = ContentQuizPair(
                title=title,
                content=content,
                quiz_questions=quiz_json,
                quiz_max_marks=max_marks
            )
            pair.save()

            return redirect('EcoWorld:gamekeeper_page')
    else:
        form = GuidesForm()
    return render(request, 'guides/add_guide.html', {'form': form})

@login_required
def menu_view(request):
    """
    This view displays the menu of available content-quiz pairs and
    their completion status for the logged-in user.

    Attributes:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders the menu page with the list of
        content-quiz pairs and user information.

    author:
        Johnny Say (js1687@exeter.ac.uk)
    """
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
    """
    This view displays the content of a specific content-quiz pair.

    Attributes:
        request (HttpRequest): The request object.
        pair_id (int): The ID of the content-quiz pair to display.

    Returns:
        HttpResponse: Renders the content page with the content-quiz
        pair and user information.

    author:
        Johnny Say (js1687@exeter.ac.uk)
    """
    pair = get_object_or_404(ContentQuizPair, id=pair_id)
    
    # Convert markdown content to HTML and mark as safe
    pair.html_content = mark_safe(markdown.markdown(pair.content))
    
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
    """
    This view displays the quiz associated with a specific content-quiz
    pair.

    Attributes:
        request (HttpRequest): The request object.
        pair_id (int): The ID of the content-quiz pair whose quiz is to
        be displayed.

    Returns:
        HttpResponse: Renders the quiz page with the quiz questions and
        user information.

    author:
        Johnny Say (js1687@exeter.ac.uk)
    """
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

    quiz_questions_json = pair.quiz_questions

    return render(request, 'guides/quiz.html', {
        'pair': pair,
        'quiz_questions_json': quiz_questions_json,
        'userinfo': userinfo[0]
    })

@login_required
def registerScore_view(request, pair_id):
    """
    This view registers the score of a user's quiz attempt and updates
    their best result and coins if applicable.

    Attributes:
        request (HttpRequest): The request object containing the quiz
            score.
        pair_id (int): The ID of the content-quiz pair associated with
            the quiz.

    Returns:
        JsonResponse: A JSON response indicating the status and
            redirect URL.

    author:
        Johnny Say (js1687@exeter.ac.uk)
    """
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

    if result.previous_best < pair.quiz_max_marks and score == pair.quiz_max_marks:
        user = User.objects.get(id=user.id)
        user.profile.number_of_coins += coins_reward
        user.save()

    result.save()
    Post.create_from_guide(pair.title, pair.content, user, score/pair.quiz_max_marks *100)

    return JsonResponse({'status': 'success', 'redirect_url': f'/guides/results/{pair_id}/'})

@login_required
def results_view(request, pair_id):
    """
    This view displays the results of a user's quiz attempt.

    Attributes:
        request (HttpRequest): The request object.
        pair_id (int): The ID of the content-quiz pair associated with
            the quiz.

    Returns:
        HttpResponse: Renders the results page with the user's score,
            previous best, and maximum marks.

    author:
        Johnny Say (js1687@exeter.ac.uk)
    """
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