"""
this module defines the views used in this app:
    -show_garden : This view renders the garden.html page to allow the user to view their garden
    -remove_card : This view removes a card from a garden square
    -getAvailableCards : This view returns the cards available to the user
    -addCard : This view adds a card to a garden square
Author:
    -Lewis Farley (lf507@exeter.ac.uk)
"""

from venv import logger
from django.shortcuts import render
from .models import garden, gardenSquare
from django.http import JsonResponse
from EcoWorld.models import ownsCard,card, User
import json
from django.core import serializers

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.conf import settings
@login_required
def show_garden(request):
    """
    Function to show the gardens page when loading into the garden. As well as this it gets all the info about the garden for that
    user along with basic user info for the header and gets the players inventory for the right side of the page
    Returns:
    Render request, the template, the garden size, userinfo and player inventory

    Author:
    Chris Lynch (cl1037@exeter.ac.uk)
    Lewis Farley (lf507@exeter.ac.uk)
    """
    g = garden.objects.get(userID=request.user)
    squares = g.gardensquare_set.all()
    processedSquares = [[squares[i * g.size + j] for j in range(g.size)] for i in range(g.size)]

    user = request.user
    user = User.objects.get(id=user.id)
    pfp_url = "/media/pfps/" + user.profile.profile_picture

    userinfo = {
        "username": user.username,
        "pfp_url": pfp_url,
        "coins": user.profile.number_of_coins
    }

 
    playerInventoryStorage = ownsCard.objects.filter(user=request.user).values(
        'card__title', 'card__image', 'quantity', 'card__id'
    )

    playerItems = [item for item in playerInventoryStorage if item["quantity"] > 0]

    return render(request, 'Garden/garden.html', {
        'squares': processedSquares,
        'MEDIA_URL': settings.MEDIA_URL,
        'size': g.size,
        "userinfo": userinfo,
        "playerInventory": playerItems 
    })


"""
Function to add a card into the garden. It takes the card id and image from inventory along with the row and col of the garden square
From here it checks to see if the card is valid before adding the card to the square and then removing one from the inventory
Returns:
The card image for the script
Author:
Chris Lynch (cl1037@exeter.ac.uk)
"""  

def addCard(request):
    
    if request.method == "POST":
        data = json.loads(request.body)

        row = int(data["row"])
        col = int(data["col"])
        card_id = int(data["card_id"]) 
        user = request.user

        try:
           
            selected_card = card.objects.get(id=card_id)

           
            owned_card = ownsCard.objects.get(user=user, card=selected_card)
            if owned_card.quantity <= 0:
                return JsonResponse({"success": False, "message": "You don't have enough of this card."})

            
            g = garden.objects.get(userID=user)
            squareID = (row - 1) * g.size + (col - 1) 
            square, created = gardenSquare.objects.get_or_create(gardenID=g, squareID=squareID)  


            
            if square.cardID is not None:
                return JsonResponse({"success": False, "message": "This square is already occupied."})

        
            square.cardID = selected_card
            square.save()

            
            owned_card.quantity -= 1
            owned_card.save()

            
            return JsonResponse({
                "success": True,
                "message": "Card placed successfully!",
                "card_image": f"/media/{selected_card.image}" 
            })

        except card.DoesNotExist:
            print("Error: Card does not exist!")  
            return JsonResponse({"success": False, "message": "Invalid card ID."})
        except gardenSquare.DoesNotExist:
            print("Error: Garden square does not exist!")  
            return JsonResponse({"success": False, "message": "Invalid garden square."})
        except ownsCard.DoesNotExist:
            print("Error: User does not own this card!") 
            return JsonResponse({"success": False, "message": "You don't own this card."})

    return JsonResponse({"success": False, "message": "Invalid request."})


def removeCard(request):
    """
    Function which removes a card when left clicked on. 
    It gets the data sent from the garden about the row and column clicked on, checks if card exists,
    if it does exist then it removes it from the garden saves it and add that quantity back to user inventory
    Returns:
    Returns the card ID and image used for it incase

    Author :
    Chris Lynch (cl1037@exeter.ac.uk)
    """

    if request.method == "POST":
        data = json.loads(request.body)

        row = int(data["row"])
        col = int(data["col"])
        user = request.user

        try:
            g = garden.objects.get(userID=user)
            squareID = (row - 1) * g.size + (col - 1)  
            square = gardenSquare.objects.get(gardenID=g, squareID=squareID)

            if square.cardID is None:
                return JsonResponse({"success": False, "message": "No card in this square."})

            
            selected_card = square.cardID
            card_id = selected_card.id  

            print(f"Removing card {selected_card.title} (ID: {card_id}) from Row: {row}, Col: {col}")

            owned_card, created = ownsCard.objects.get_or_create(user=user, card=selected_card)
            owned_card.quantity += 1
            owned_card.save()

            
            square.cardID = None
            square.save()

            return JsonResponse({
                "success": True,
                "message": "Card removed successfully!",
                "card_id": card_id, 
                "card_image": f"/media/{selected_card.image}" 
            })

        except gardenSquare.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid garden square."})
        except card.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid card."})
        except ownsCard.DoesNotExist:
            return JsonResponse({"success": False, "message": "You don't own this card."})

    return JsonResponse({"success": False, "message": "Invalid request."})
