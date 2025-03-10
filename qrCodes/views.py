from django.shortcuts import render
from EcoWorld.models import waterFountain,drinkEvent
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.conf import settings
# Create your views here.
@permission_required("Accounts.can_view_admin_button")  # Only allowed admins can generate new QR codes
def generate_qr_code(request):
    fountains = waterFountain.objects.all() 
    print(fountains)
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
    print("lastEvent")
    print(last_drink)
    if last_drink:
        print("last drink not none")
        time_difference = timezone.now() - last_drink.drank_on
        if time_difference < settings.DRINKING_COOLDOWN:
            return render(request, 'drink_cooldown_page.html')
    # More than 20 minutes have passed
    print("User drank more than 20 minutes ago")
    drinkEvent.objects.create(user=user,fountain=waterFountain.objects.get(id=fountain_id))
    print(fountain_id)
    user.profile.number_of_coins += settings.VALUE_OF_DRINK
    user.profile.save()
    
    return render(request, 'drink_registered.html')
        
