from django.shortcuts import render, redirect
from .models import drinkEvent,User,waterFountain
import json
from qr_code.qrcode.utils import QRCodeOptions
from django.http import HttpResponse
from .forms import WaterBottleFillForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def addDrink(request):
    print("add drink post req")
    if request.method == "POST":
        data = json.loads(request.body)
        user = data["user"]
        fountain = data["fountain"]
        drank_on = data["drank_on"]
        print(f'request with body {data}')
        user = User.objects.get(id=user)
        fountain = waterFountain.objects.get(id=fountain)
        if user is None or fountain is None:
            return HttpResponse("Invalid user or fountain")
        
        drinkEvent.objects.create(user=user,fountain=fountain,drank_on=drank_on)

        return HttpResponse("Added drink event")
    return HttpResponse("Invalid request type 2")

def testAddDrink(request):
    print("add drink post req")
    return render(request, "EcoWorld/addDrink.html")

def generate_qr_code(request):
    qr_options = QRCodeOptions(size='M' , border=6, error_correction='L')
    qr_data = "https://EcoWorld.com/scan/" #Change this to website name I have no idea
    return render(request, 'EcoWorld/qr_code.html', {'qr_data': qr_data, 'qr_option': qr_options})

def scan_qr_code(request):
    return render(request, 'EcoWorld/scan_qr_code.html')

def upload_bottle_photo(request):
    if request.method == 'POST':
        form = WaterBottleFillForm(request.POST, request.FILES)
        if form.is_valid():
            water_fill = form.save(commit=False)
            water_fill.user = request.user
            water_fill.save()
            return redirect('success_page') #Create a success page
    else:
        form = WaterBottleFillForm()

    return render(request, 'EcoWorld/upload_photo.html', {'form': form})

