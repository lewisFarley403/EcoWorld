from django.shortcuts import render
from .models import drinkEvent,User,waterFountain,pack,ownsCard
import json
from django.http import HttpResponse
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
        inventory =ownsCard.objects.create(user=user,card=card)
        inventory.quantity += 1
        inventory.save()
        # return card as json
        return HttpResponse(json.dumps({"title": card.title, "description": card.description, "rarity": card.rarity.title, "image": card.image.url}))

    elif request.method == "GET":
        packs = pack.objects.all()
        return render(request, "ecoWorld/store.html",{ "packs": packs })
    return HttpResponse("Invalid request")