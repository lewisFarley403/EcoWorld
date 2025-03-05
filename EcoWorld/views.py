"""
this module defines the views used in this app:
    - `addDrink` : This view allows the user to add a drink event
    - `testAddDrink` : This view allows the user to test adding a drink event (for testing purposes)
Author:
    -Lewis Farley (lf507@exeter.ac.uk)
    -Chris Lynch (cl1037@exeter.ac.uk)
"""

from django.shortcuts import render, redirect
from .models import drinkEvent,User,waterFountain,pack,ownsCard,challenge,ongoingChallenge
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .utils import getUsersChallenges
from datetime import datetime
# from qr_code.qrcode.utils import QRCodeOptions
from .forms import WaterBottleFillForm

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


def dashboard(request):
    """
    Dashboard on request takes user info to send to dashboard
    Returns: render request and userinfo to be displayed

    Author: 
    Chris Lynch (cl1037@exeter.ac.uk)
    """

    #Upon loading the page the dashboard needs its username and pfp along with coins, this function here gives it to the dashboard html file
    if request.method == "GET":
        user = request.user
        user = User.objects.get(id=user.id)
        pfp_url = user.profile.profile_picture
        pfp_url = "/media/pfps/" + pfp_url

        userinfo = []
        userinfo.append({
            "username": user.username,
            "pfp_url": pfp_url,
            "coins" : user.profile.number_of_coins
            })

        return render(request, "EcoWorld/dashboard.html", {"userinfo":userinfo[0]})

def generate_qr_code(request):
    """
    This Generates a QR code and renders it on a template (For functionality)
    """
    qr_options = QRCodeOptions(size='M' , border=6, error_correction='L')
    qr_data = "https://EcoWorld.com/scan/" #Change this to website name I have no idea
    return render(request, 'EcoWorld/qr_code.html', {'qr_data': qr_data, 'qr_options': qr_options})

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

@login_required
def store(request):
    """
    This view renders the store for the ecoworld page. This pages purpose is to allow users to purchase packs to unlock cards with their coins
    It requires the user to be logged in
    Returns:
    Render request plus two dictionaries one of user data for the header and one of the pack data for viewing
    Author:
    Chris Lynch (cl1037@exeter.ac.uk)
    
    """
    if request.method == "GET":
        packs = pack.objects.all()
        pack_list = []
        #Gets all info from each of the 3 packs
        for pack_ in packs:
            image_url = pack_.packimage.url
            id = pack_.id
            #Adds the pack info to the list
            pack_list.append({
                "id" : id,
                "title": pack_.title,
                "cost" : pack_.cost,
                "image_url": image_url,
                "common_prob": pack_.commonProb,
                "rare_prob": pack_.rareProb,
                "epic_prob": pack_.epicProb,
                "legendary_prob": pack_.legendaryProb,
                "color_class": pack_.color_class,

            })
        
        #Function to get the user data and then adds it to the user dictionary
        user = request.user
        user = User.objects.get(id=user.id)
        pfp_url = user.profile.profile_picture
        pfp_url = "/media/pfps/" + pfp_url

        userinfo = []
        userinfo.append({
            "username": user.username,
            "pfp_url": pfp_url,
            "coins" : user.profile.number_of_coins
            })
        
        #Sends the info to the page
        return render(request, "ecoWorld/store.html",{ "packs": pack_list, "userinfo": userinfo[0]})
    
    return HttpResponse("Invalid request")


@login_required
def buy_pack(request):
    """
    Function to handle purchasing a pack and making sure the user can
    Returns:
    Appropriate error if error
    No coins if the user doesnt have enough
    Success if it can be bought

    Author: 
    Chris Lynch (cl1037@exeter.ac.uk)
    """
    if request.method == "POST":
        #Error handling where it tries to get the appropriate data
        try:
            data = json.loads(request.body)
            user = request.user
            pack_id = data.get("pack_id")
            try:
                selected_pack = pack.objects.get(id=pack_id)
            except pack.DoesNotExist:
                return JsonResponse({"error": "Invalid pack selected"}, status=400)

            #Checks if user can buy the pack
            if selected_pack.cost > user.profile.number_of_coins:
                return JsonResponse({"error": "Insufficient coins"}, status=400)

            #If pack found it takes the coins out and gives success
            user.profile.number_of_coins -= selected_pack.cost
            user.profile.save()

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def pack_opening_page(request):
    """
    Webpage to render the pack opening animation. When a pack is bought it redirects to here where it will send the correct info 
    to the page so the right pack gets opened
    It has a function to buy pack from the packs model in models.py
    Returns:
    Bought pack card won

    Author:
    Chris Lynch (cl1037@exeter.ac.uk)
    
    """
    #Gets pack id
    pack_id = request.GET.get("pack_id")
    #Error checks if it works
    try:
        selected_pack = pack.objects.get(id=pack_id)
    except pack.DoesNotExist:
        return JsonResponse({"error": "Invalid pack ID"}, status=400)
    
    #Card received variable when opening a pack, adds to inventory and saves
    card_received = selected_pack.openPack()
    inventory, _ = ownsCard.objects.get_or_create(user=request.user, card=card_received)
    inventory.quantity += 1
    inventory.save()


    #Image of the card won to return to the page
    image_url = card_received.image.url
    return render(request, "EcoWorld/pack_opening_page.html", {"image": image_url})




@login_required
def challenge(request):
    challenges = getUsersChallenges(request.user)
    user = User.objects.get(id=request.user.id)
    print(type(user.username)) 
    print(user.profile.number_of_coins)   
    return render(request, "EcoWorld/challengePage.html", {"challenges":challenges,'username':user.username,'coins':user.profile.number_of_coins})
@login_required
def completeChallenge(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(request.user.id)
        user = User.objects.get(id=request.user.id)
        onGoingChallenge = data["id"]
        print(f"User: {user}")
        print(f"Challenge: {challenge}")
        chal = ongoingChallenge.objects.get(id=onGoingChallenge)
        worth = chal.challenge.worth
        chal.submitted_on = datetime.now()
        
        user.profile.number_of_coins += worth
        user.save()
        chal.save()
        return HttpResponse("Challenge completed")
    return HttpResponse("Invalid request type")

@login_required
def friends(request):
    if request.method == "GET":
        user = request.user
        user = User.objects.get(id=user.id)
        pfp_url = user.profile.profile_picture
        pfp_url = "/media/pfps/" + pfp_url

        userinfo = []
        userinfo.append({
            "username": user.username,
            "pfp_url": pfp_url,
            "coins" : user.profile.number_of_coins
            })
            
        return render(request, "EcoWorld/friends.html", {"userinfo" : userinfo[0]})
    
    elif request.method == "POST":

        #Gets user data for the navbar
        user = request.user
        user = User.objects.get(id=user.id)
        pfp_url = user.profile.profile_picture
        pfp_url = "/media/pfps/" + pfp_url

        userinfo = []
        userinfo.append({
            "username": user.username,
            "pfp_url": pfp_url,
            "coins" : user.profile.number_of_coins
            })
        
        #Get the username sent in the form
        username = request.POST.get("friendUsername")
    
        return render(request, "EcoWorld/friends.html", {"userinfo": userinfo[0]})