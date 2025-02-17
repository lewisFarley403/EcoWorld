"""
this module defines the views used in this app:
    -show_garden : This view renders the garden.html page to allow the user to view their garden
    -remove_card : This view removes a card from a garden square
    -getAvailableCards : This view returns the cards available to the user
    -addCard : This view adds a card to a garden square
Author:
    -Lewis Farley (lf507@exeter.ac.uk)
"""

from django.shortcuts import render
from .models import garden
from django.http import JsonResponse
from EcoWorld.models import ownsCard,card
import json
from django.core import serializers

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.conf import settings
@login_required  # Ensure that only logged-in users can access the profile
def show_garden(request):
    """
    This view renders the garden.html page to allow the user to view their garden.
    It requires the user to be logged in. If the user is not logged in, it redirects to the login page.
    Attributes:
        request : HttpRequest : The HTTP request object
    Returns:
        render : HttpResponse : The rendered HTML page
    Author:
        - Lewis Farley (lf507@exeter.ac.uk)
    """
    g = garden.objects.get(userID=request.user)
    squares = g.gardensquare_set.all()
    processedSquares = [[squares[i*g.size+j] for j in range (g.size)] for i in range (g.size)]


    playerInventory = ownsCard.objects.filter(user=request.user)
    availableCards = [ card.card for card in playerInventory if card.card not in [square.cardID for square in squares]]
    serialized=json.loads(serializers.serialize('json', availableCards))
    final = [obj["fields"]|{'id':obj['pk']} for obj in serialized]

    return render(request, 'Garden/garden.html', {'squares': processedSquares,'MEDIA_URL':settings.MEDIA_URL,'size':g.size,'availableCards':final})
def remove_card(request):
    """
    Removes a card from the users garden square,
    with the coordinate of this square being passed in the body of the request
    Attributes:
        request : HttpRequest : The HTTP request object
    Returns:
        JsonResponse : The JSON response object
    Author:
        - Lewis Farley (lf507@exeter.ac.uk)
    """
    if request.method =="POST":
        body =json.loads(request.body)
        row = int(body['row'])
        col = int(body['col'])
        g = garden.objects.get(userID=request.user)
        squareID = (row-1)*g.size+(col-1)
        square = g.gardensquare_set.get(gardenID=g,squareID=squareID)
        square.cardID = None
        square.save()
    # return json to say success    
    return JsonResponse({'success': True, 'message': 'Card removed!'})
def getAvailableCards(request):
    g = garden.objects.get(userID=request.user)
    squares = g.gardensquare_set.all()
    playerInventory = ownsCard.objects.filter(user=request.user)
    # availableCards = [ card.card for card in playerInventory if card.card not in [square.cardID for square in squares]]

    # with new db that has quantity
    availableCards = [ card.card for card in playerInventory if card.quantity>0 and card.card not in [square.cardID for square in squares]]
    serialized=json.loads(serializers.serialize('json', availableCards))
    final = [obj["fields"] for obj in serialized]
    return JsonResponse({'success': True,'cards':final})

def addCard(request):
    """
    This view adds a card to a square in the users garden.
    The row, col and cardID to be added are placed in the body of the request
    Attributes:
        request : HttpRequest : The HTTP request object
    Returns:
    
    """
    if request.method =="POST":
        body = json.loads(request.body)
        g=garden.objects.get(userID=request.user)
        row = int(body['row'])
        col = int(body['col'])
        cardID = int(body['cardID'])
        c = card.objects.get(id=cardID)
        squareID = (row-1)*g.size+(col-1)
        square = g.gardensquare_set.get(gardenID=g,squareID=squareID)
        square.cardID = c
        # maybe check if this quantity is >0
        ownsCard.objects.get(user=request.user,card=c).quantity-=1
        ownsCard.objects.get(user=request.user,card=c).save()
        square.save()
        return JsonResponse({'success': True, 'message': 'Card added!'})