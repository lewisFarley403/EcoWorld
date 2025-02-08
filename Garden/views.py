from django.shortcuts import render
from .models import garden
from django.http import JsonResponse
from EcoWorld.models import ownsCard
import json
from django.core import serializers

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.conf import settings
@login_required  # Ensure that only logged-in users can access the profile
def show_garden(request):
    print(type(request.user))
    g = garden.objects.get(userID=request.user)
    squares = g.gardensquare_set.all()
    print(list(squares))
    processedSquares = [[squares[i*g.size+j] for j in range (g.size)] for i in range (g.size)]
    print(processedSquares)
    return render(request, 'Garden/garden.html', {'squares': processedSquares,'MEDIA_URL':settings.MEDIA_URL,'size':g.size})
def remove_card(request):
    if request.method =="POST":
        print("REQUEST IS POST")
        print(request.POST)
        body =json.loads(request.body)
        row = int(body['row'])
        col = int(body['col'])
        g = garden.objects.get(userID=request.user)
        squareID = (row-1)*g.size+(col-1)
        square = g.gardensquare_set.get(gardenID=g,squareID=squareID)
        
        print("SQUARE BELLOW")
        print(squareID)
        print(square)
        square.cardID = None
        square.save()
    # return json to say success    
    return JsonResponse({'success': True, 'message': 'Card removed!'})
def getAvailableCards(request):
    g = garden.objects.get(userID=request.user)
    squares = g.gardensquare_set.all()
    playerInventory = ownsCard.objects.filter(user=request.user)
    availableCards = [ card.card for card in playerInventory if card.card not in [square.cardID for square in squares]]
    # print(dir(availableCards))
    # availableCards = []
    # for square in squares:
    #     if square.cardID is None:
    #         availableCards.append(square.squareID)
    serialized=json.loads(serializers.serialize('json', availableCards))
    print("SERIALIZED")
    final = [obj["fields"] for obj in serialized]
    print(final)
    print("SERIALIZED bellow")
    return JsonResponse({'success': True,'cards':final})