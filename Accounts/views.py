# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileUpdateForm
from .models import Profile
from .utils import createGarden
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            print("User: ")
            print(user)
            # create garden for user
            createGarden(user)
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'Accounts/signup.html', {'form': form})

@login_required  # Ensure that only logged-in users can access the profile
def profile(request):
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

    # If it's a GET request, show the form
    return render(request, 'Accounts/profile.html', {'profile': profile})
