from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import WaterFountainForm
from .models import waterFountain, drinkEvent

# Create your views here.
@permission_required("Accounts.can_view_gamekeeper_button")  # Only allowed gamekeepers can generate new QR codes
def generate_qr_code(request):
    fountains = waterFountain.objects.all() 
    return render(request, 'make_qr_code.html', {'fountains': fountains,
                                                      'width':settings.QR_CODE_WIDTH,
                                                      'height':settings.QR_CODE_HEIGHT})
@login_required
def scan_code_page(request):
    return render(request, 'qr_scanner.html')

@login_required
def scan_code(request):
    user = request.user
    fountain_id = request.GET.get('id')
    last_drink = drinkEvent.objects.filter(user=user).order_by('-drank_on').first()
    if last_drink:
        time_difference = timezone.now() - last_drink.drank_on
        if time_difference < settings.DRINKING_COOLDOWN:
            return redirect( "EcoWorld:challenge")
    # More than 20 minutes have passed
    drinkEvent.objects.create(user=user,fountain=waterFountain.objects.get(id=fountain_id))
    user.profile.number_of_coins += settings.VALUE_OF_DRINK
    user.profile.save()
    
    return render(request, 'drink_registered.html')

@permission_required("Accounts.can_view_gamekeeper_button")
def add_water_fountain(request):
    if request.method == "POST":
        form = WaterFountainForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("EcoWorld:gamekeeper_page")
    else:
        form = WaterFountainForm()

    return render(request, 'add_water_fountain.html', {'form': form})
        
