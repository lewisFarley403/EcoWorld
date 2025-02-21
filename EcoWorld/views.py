"""
this module defines the views used in this app:
    - `addDrink` : This view allows the user to add a drink event
    - `testAddDrink` : This view allows the user to test adding a drink event (for testing purposes)
Author:
    -Lewis Farley (lf507@exeter.ac.uk)
    -Chris Lynch (cl1037@exeter.ac.uk)
"""

from django.shortcuts import render
from .models import drinkEvent,User,waterFountain,pack,ownsCard,challenge,ongoingChallenge
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .utils import getUsersChallenges
from datetime import datetime

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
    return render(request, "EcoWorld/dashboard.html")

def testAddDrink(request):

    print("add drink post req")
    return render(request, "ecoWorld/addDrink.html")

@login_required
def store(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        p = data["pack"]
        user = User.objects.get(id=user.id)
        p = pack.objects.get(id=p)
        if user is None or p is None:
            return HttpResponse("Invalid user or pack")
        if p.cost > user.profile.number_of_coins:
            return HttpResponse("Insufficient coins")
        user.profile.number_of_coins -= p.cost
        user.profile.save()
        card = p.openPack()
        inventory =ownsCard.objects.get(user=user,card=card)
        inventory.quantity += 1
        inventory.save()
        title= card.title
        # return card as json
        return HttpResponse(json.dumps({"title": title, "description": card.description, "rarity": card.rarity.title, "image": card.image.url}))

    elif request.method == "GET":
        packs = pack.objects.all()
        pack_list = []
        for pack_ in packs:
            image_url = pack_.packimage.url
            id = pack_.id

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
            
        user = request.user
        user = User.objects.get(id=user.id)
        username = user.username
        pfp_url = user.profile.profile_picture
        pfp_url = "/media/pfps/" + pfp_url

        userinfo = []
        userinfo.append({
            "username": user.username,
            "pfp_url": pfp_url,
            "coins" : user.profile.number_of_coins
            })
        print(pfp_url)


        

        return render(request, "ecoWorld/store.html",{ "packs": pack_list, "userinfo": userinfo[0]})
    
    return HttpResponse("Invalid request")


@login_required
def buy_pack(request):
    """Handles pack purchase validation before redirecting to the opening screen."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user
            pack_id = data.get("pack_id")
            try:
                selected_pack = pack.objects.get(id=pack_id)
            except pack.DoesNotExist:
                return JsonResponse({"error": "Invalid pack selected"}, status=400)

            if selected_pack.cost > user.profile.number_of_coins:
                return JsonResponse({"error": "Insufficient coins"}, status=400)

            user.profile.number_of_coins -= selected_pack.cost
            user.profile.save()

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def pack_opening_page(request):
    pack_id = request.GET.get("pack_id")
    
    try:
        selected_pack = pack.objects.get(id=pack_id)
    except pack.DoesNotExist:
        return JsonResponse({"error": "Invalid pack ID"}, status=400)
    
    card_received = selected_pack.openPack()
    inventory, _ = ownsCard.objects.get_or_create(user=request.user, card=card_received)
    inventory.quantity += 1
    inventory.save()

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

