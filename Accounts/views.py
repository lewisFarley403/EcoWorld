"""
module defines views for the Accounts app:
    - `signup` : This view allows the user to sign up for an account
    - `profile` : This view allows the user to view and update their profile
author:
    - Ethan Sweeney (es1052@exeter.ac.uk) 
"""
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect

from EcoWorld.models import ownsCard
from Garden.models import garden
from .forms import SignUpForm
from .models import Profile
from .utils import create_garden, create_owns_db

#pylint: disable=too-few-public-methods
# pylint: disable=no-member

# views.py


def privacy_policy(request):

    """
    This view renders the privacy policy page.
    Attributes:
        request : HttpRequest : The HTTP request object
    Returns:
        render : HttpResponse : The rendered HTML page
    """
    return render(request, 'Accounts/privacy_policy.html')


def signup(request):
    """
    This view allows the user to sign up for an account.
    It renders the signup form (when it received get request)
    and creates a new user when the form is submitted (it receives post request).

    Attributes:
        request : HttpRequest : The HTTP request object
    Returns:
        render : HttpResponse : The HTTP response object
    Author:
        Ethan Sweeney (es1052@exeter.ac.uk)
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            # create garden for user
            create_garden(user)
            #creates cards owned by user set default as 0.
            create_owns_db(user)
            login(request, user)
            return redirect('/ecoworld/')
            # Redirect to the login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'Accounts/signup.html', {'form': form})

@login_required  # Ensure that only logged-in users can access the profile
def profile(request):
    """
    This view allows the user to view and update their profile.
    It renders the profile form (when it received get request)
    and updates the profile when the form is submitted (it receives post request).
    it requires the user to be logged in. if the user is not logged in,
    it redirects to the login page.
    Attributes:
        request : HttpRequest : The HTTP request object
    Returns:
        render : HttpResponse : The rendered HTML page
    Author:
        - Ethan Sweeney (es1052@exeter.ac.uk)

    """
    profile = Profile.objects.get(user=request.user)

    # Handle the profile picture update
    if request.method == 'POST':
        # Get the form data
        bio = request.POST.get('bio')
        profile_picture = request.POST.get('profile_picture')

        # Update the profile

        profile.bio = bio
        if profile_picture:
            profile.profile_picture = profile_picture
            # Set the selected profile picture file name
        profile.save()

        # Redirect to the profile page after saving
        return redirect('profile')

    g = garden.objects.get(userID=request.user)
    squares = g.gardensquare_set.all()
    processed_squares = [[squares[i*g.size+j] for j in range (g.size)] for i in range (g.size)]


    player_inventory = ownsCard.objects.filter(user=request.user)
    available_cards = [ card.card for card in player_inventory if card.card not in
                       [square.cardID for square in squares]]
    serialized=json.loads(serializers.serialize('json', available_cards))
    final = [obj["fields"]|{'id':obj['pk']} for obj in serialized]

    # If it's a GET request, show the form
    return render(request, 'Accounts/profile.html',
                  {'profile': profile,'squares': processed_squares,'MEDIA_URL'
                  :settings.MEDIA_URL,'size':g.size,'available_cards':final})

@login_required
def user_info(request):
    """
    This view returns the user information in JSON format.
    Attributes:
        request : HttpRequest : The HTTP request object
    Returns:
        JsonResponse : HttpResponse : The JSON response object
    Author:
        - Lewis Farley (lf507@exeter.ac.uk)
    """
    user_info = {
        'username': request.user.username,
        'pfp_url': "/media/pfps/" + request.user.profile.profile_picture
        if request.user.profile.profile_picture else '',
        'coins': request.user.profile.number_of_coins,
    }
    return JsonResponse(user_info)


def read_only_profile(request):
    """
    This view allows the user to view the user_profile of another user.
    Attributes:
        request : HttpRequest : The HTTP request object
        username : str : The username of the user whose user_profile is being viewed
    Returns:
        render : HttpResponse : The rendered HTML page
    Author:
        - Lewis Farley (lf507@exeter.ac.uk)
    """
    username = request.GET.get("username", None)  # Default if no username is provided

    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    g = garden.objects.get(userID=user)
    squares = g.gardensquare_set.all()
    processed_squares = [[squares[i * g.size + j] for j in range(g.size)]
                        for i in range(g.size)]
    return render(request, 'Accounts/profile.html',
                  {'user_profile': user_profile, 'squares': processed_squares,
                   'MEDIA_URL': settings.MEDIA_URL, 'size': g.size,'is_read_only':
                       True,'username':username})



@login_required
def delete_account(request):
    """
    This view allows the user to delete their account.
    Attributes:
        request : HttpRequest : The HTTP request object
    Returns:
        redirect : HttpResponse : The HTTP page at the base URL
    Author:
        - Ethan Sweeney (es1052@exeter.ac.uk)
    """
    user = request.user
    logout(request)  # Log out the user before deleting
    user.delete()  # Delete the user from the database
    messages.success(request, 'Your account has been deleted successfully.')
    return redirect('/')  # Redirect to login page


@login_required
def logout_view(request):
    """
    This view logs out the user and redirects them to the home page.

    Attributes:
        request : HttpRequest : The HTTP request object
    Returns:
        redirect : HttpResponse : The HTTP response redirecting to the home page
    Author:
        - Ethan Sweeney (es1052@exeter.ac.uk)
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/')
