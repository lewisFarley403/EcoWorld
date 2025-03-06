"""
module defines views for the Accounts app:
    - `signup` : This view allows the user to sign up for an account
    - `profile` : This view allows the user to view and update their profile
author:
    - Ethan Sweeney (es1052@exeter.ac.uk) 
"""
from django.contrib import messages
# views.py

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Profile
from .utils import createGarden, createOwnsDb
from Garden.models import garden
from EcoWorld.models import ownsCard
import json
from django.core import serializers
from django.conf import settings
from django.http import JsonResponse



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
    It renders the signup form (when it received get request) and creates a new user when the form is submitted (it receives post request).

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
            print("User: ")
            print(user)
            # create garden for user
            createGarden(user)
            #creates cards owned by user set default as 0.
            createOwnsDb(user)
            login(request, user)
            return redirect('/ecoworld/')  # Redirect to the login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'Accounts/signup.html', {'form': form})

@login_required  # Ensure that only logged-in users can access the profile
def profile(request):
    """
    This view allows the user to view and update their profile.
    It renders the profile form (when it received get request) and updates the profile when the form is submitted (it receives post request).
    it requires the user to be logged in. if the user is not logged in, it redirects to the login page.
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
            profile.profile_picture = profile_picture  # Set the selected profile picture file name
        profile.save()

        # Redirect to the profile page after saving
        return redirect('profile')

    g = garden.objects.get(userID=request.user)
    squares = g.gardensquare_set.all()
    processedSquares = [[squares[i*g.size+j] for j in range (g.size)] for i in range (g.size)]


    playerInventory = ownsCard.objects.filter(user=request.user)
    availableCards = [ card.card for card in playerInventory if card.card not in [square.cardID for square in squares]]
    serialized=json.loads(serializers.serialize('json', availableCards))
    final = [obj["fields"]|{'id':obj['pk']} for obj in serialized]

    # If it's a GET request, show the form
    return render(request, 'Accounts/profile.html', {'profile': profile,'squares': processedSquares,'MEDIA_URL':settings.MEDIA_URL,'size':g.size,'availableCards':final})

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
    # pfp_url = "/media/pfps/" + pfp_url
    user_info = {
        'username': request.user.username,
        'pfp_url': "/media/pfps/" +request.user.profile.profile_picture if request.user.profile.profile_picture else '',
        'coins': request.user.profile.number_of_coins,
    }
    return JsonResponse(user_info)



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