from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from .models import GlassDisposalEntry, RecyclingLocation
from .forms import GlassDisposalForm
import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates the distance between two points on the earths surface

    Parameters:
        lat1 (float): The latitude of the first point
        lon1 (float): The longitude of the first point
        lat2 (float): The latitude of the second point
        lon2 (float): The longitude of the second point

    Returns:
        float: The distance between the two points

    Author:
        Charlie Shortman
    """
    r = 6371000  #earths radius
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return r * c  #distance

@login_required
def submit_disposal(request):
    """
    Handles glass disposal submissions with location validation

    Ensures that users submit their disposal within 100m of a registered recycling location
    Awards coins based on how many bottles are recycled

    Methods:
        POST: Processes the form submission, validates location, and awards coins
        GET: Displays the glass disposal form

    Parameters:
        request: The request object containing user data and submission details

    Returns:
        HttpResponse: Renders the disposal form or redirects to the thankyou page if successful

    Author:
        Charlie Shortman
    """
    if request.method == 'POST':
        form = GlassDisposalForm(request.POST, request.FILES)
        user_lat = float(request.POST.get('latitude', 0))
        user_lon = float(request.POST.get('longitude', 0))

        if form.is_valid():
            nearest_location = None
            min_distance = float('inf')

            for location in RecyclingLocation.objects.all():
                distance = haversine(user_lat, user_lon, location.latitude, location.longitude)
                if distance < min_distance:
                    min_distance = distance
                    nearest_location = location

            if min_distance > 100:  #user is outside 100m range
                return render(request, 'glassDisposal/submit_disposal.html', {
                    'form': form,
                    'error': "You are not near a valid recycling location!"
                })

            disposal_entry = form.save(commit=False)
            disposal_entry.user = request.user
            disposal_entry.recycling_location = nearest_location
            disposal_entry.coins_awarded = disposal_entry.bottle_count * settings.GLASS_DISPOSAL_REWARD_PER_BOTTLE
            disposal_entry.save()

            request.user.profile.number_of_coins += disposal_entry.coins_awarded
            request.user.profile.save()

            return redirect('thankyou', coins_earned=disposal_entry.coins_awarded)

    else:
        form = GlassDisposalForm()

    return render(request, 'glassDisposal/submit_disposal.html', {'form': form})


def thankyou(request, coins_earned):
    """
    Renders the thankyou page displaying the number of coins earned

    Parameters:
        request: The request object
        coins_earned (int): Number of coins awarded to the user

    Returns:
        HttpResponse: Renders the thankyou page template with the earned coins

    Author:
        Charlie Shortman
    """
    return render(request, 'glassDisposal/thankyou.html', {'coins_earned': coins_earned})


@permission_required("Accounts.can_view_gamekeeper_button")
def add_recycling_point(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if name and latitude and longitude:
            RecyclingLocation.objects.create(
                name=name,
                latitude=float(latitude),
                longitude=float(longitude)
            )
            return redirect('EcoWorld:gamekeeper_page')  # Replace with your success URL or view name
    return render(request, 'glassDisposal/add_recycling_point.html')