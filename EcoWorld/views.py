"""
this module defines the views used in this app:
    - `addDrink` : This view allows the user to add a drink event
    - `testAddDrink` : This view allows the user to test adding a drink event (for testing purposes)
Author:
    -Lewis Farley (lf507@exeter.ac.uk)
    -Chris Lynch (cl1037@exeter.ac.uk)
"""
from django.contrib.auth.models import Permission
import random
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt


from .models import User, pack, ownsCard, challenge, ongoingChallenge, card, Merge
from qrCodes.models import drinkEvent
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from .utils import getUsersChallenges
from datetime import datetime
from Accounts.models import Friends, FriendRequests
from .forms import ChallengeForm
from django.db.models import Q
from django.utils.timezone import now
from datetime import date
from django.conf import settings
from forum.models import Post
# Create your views here.
def getUserInfo(request):
    """
    This function gets the user info for the navbar
    Returns: user info to be displayed on the navbar

    Author:
    Ethan Sweeney (es1052@exeter.ac.uk)
    """
    user = request.user
    user = User.objects.get(id=user.id)
    pfp_url = user.profile.profile_picture
    pfp_url = "/media/pfps/" + pfp_url

    userinfo = []
    userinfo.append({
        "username": user.username,
        "pfp_url": pfp_url,
        "coins": user.profile.number_of_coins
    })
    return userinfo


@login_required
def dashboard(request):
    """
    Dashboard on request takes user info to send to dashboard
    Returns: render request and userinfo to be displayed

    Author:
    Chris Lynch (cl1037@exeter.ac.uk)
    """

    #Upon loading the page the dashboard needs its username and pfp along with coins, this function here gives it to the dashboard html file
    if request.method == "GET":
        userinfo = getUserInfo(request)

        return render(request, "EcoWorld/dashboard.html", {"userinfo":userinfo[0]})

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
        userinfo = getUserInfo(request)

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
    Post.create_from_card(card_received, request.user)


    #Image of the card won to return to the page
    image_url = card_received.image.url
    return render(request, "EcoWorld/pack_opening_page.html", {"image": image_url})

@login_required
def challenge(request):
    daily_objectives = getUsersChallenges(request.user)
    user = User.objects.get(id=request.user.id)

    # Get the user's last drink event
    last_drink = drinkEvent.objects.filter(user=user).order_by('-drank_on').first()
    last_drink_time = last_drink.drank_on if last_drink else None

    # Check if the drink is on cooldown
    is_drink_available = True
    if last_drink_time:
        time_difference = now() - last_drink_time
        is_drink_available = time_difference >= settings.DRINKING_COOLDOWN

    today = date.today()
    total_daily_objectives = len(daily_objectives)
    completed_daily_objectives = sum(1 for c in daily_objectives if c.is_complete())

    total_objective_worth = sum(obj.challenge.goal for obj in daily_objectives)  # Total worth of all objectives
    completed_objective_worth = sum(obj.progress for obj in daily_objectives)  # Sum of completed progress
    context = {
        "daily_objectives": daily_objectives,
        "username": user.username,
        "coins": user.profile.number_of_coins,
        "today_date": today,
        "total_challenges": total_daily_objectives,
        "completed_challenges": completed_daily_objectives,
        "total_objectives": total_objective_worth,
        "completed_objectives": completed_objective_worth,
        "last_drink_time": last_drink_time,
        "is_drink_available": is_drink_available,
        "settings": {
            "DRINKING_COOLDOWN": settings.DRINKING_COOLDOWN
        }
    }
    return render(request, "EcoWorld/challenge_page.html", context)


@login_required
def increment_daily_objective(request):
    """
    Increments the progress of a daily objective by 1.
    Grants coins when an objective is completed.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        objective_id = data.get("objective_id")


        objective = ongoingChallenge.objects.get(id=objective_id, user=request.user)
        if objective.progress < objective.challenge.goal:  # Ensure it does not exceed goal
            objective.progress += 1
            objective.save()

            # If the objective is now complete, mark as completed and give coins
            if objective.progress == objective.challenge.goal:
                objective.completed = True
                request.user.profile.number_of_coins += objective.challenge.worth  # Add coins
                request.user.profile.save()
                objective.save()


            # completed_objectives_count = ongoingChallenge.objects.filter(user=request.user, completed=True).count()
            users_ongoing_challenges = ongoingChallenge.objects.filter(user=request.user)
            completed_objectives_count =0
            for challenge in users_ongoing_challenges:
                if challenge.is_complete():
                    completed_objectives_count +=1

            daily_objectives = getUsersChallenges(request.user)
            total_objective_worth = sum(obj.challenge.goal for obj in daily_objectives)  # Total worth of all objectives
            completed_objective_worth = sum(obj.progress for obj in daily_objectives)  # Sum of completed progress
            return JsonResponse({
                "success": True,
                "progress": objective.progress,
                "goal": objective.challenge.goal,
                "reward": objective.challenge.worth,
                "completed_objectives": completed_objectives_count,
                "total_objective_worth":total_objective_worth,
                "completed_objective_worth":completed_objective_worth
            })

        else:
            return JsonResponse({"success": False, "message": "Goal already reached"})
        # except ongoingChallenge.DoesNotExist:
        # except Exception as e:
        #     print(e)
        #     return JsonResponse({"success": False, "message": "Objective not found"}, status=404)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

@login_required
def completeChallenge(request):

    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(id=request.user.id)
        onging = ongoingChallenge.objects.filter(user=user)

        onGoingChallenge = data["id"]

        chal = ongoingChallenge.objects.get(id=onGoingChallenge)
        worth = chal.challenge.worth
        chal.submitted_on = datetime.now()

        user.profile.number_of_coins += worth
        user.save()
        chal.save()
        return HttpResponse("Challenge completed")
    return HttpResponse("Invalid request type")

@permission_required("Accounts.can_view_gamekeeper_button")  # Only existing gamekeeper can access
def gamekeeper_page(request):
    """
    This view renders the gamekeeper page, which allows gamekeepers to do things a regular user cannot.
    Returns: render request and a list of users who are not gamekeepers

    Author:
    Ethan Sweeney (es1052@exeter.ac.uk)
    """
    if request.method == "GET":
        userinfo = getUserInfo(request)

    users = User.objects.exclude(user_permissions__codename="can_view_gamekeeper_button")
    missing_rows = range(max(0, 3 - users.count()))
    return render(request, "EcoWorld/gamekeeper_page.html", {"users": users, "missing_rows": missing_rows, "userinfo":userinfo[0]})

@permission_required("Accounts.can_view_gamekeeper_button")  # Only gamekeepers can promote others
def grant_gamekeeper(request, user_id):
    """
    This view grants the can_view_gamekeeper_button permission to a user, effectively promoting them to an gamekeeper.

    Returns: Reloading of the gamekeeper page with the updated list of users.

    Author:
    Ethan Sweeney (es1052@exeter.ac.uk)
    """
    if not request.user.has_perm("Accounts.can_view_gamekeeper_button"):
        return HttpResponse("You do not have permission to do this.", status=403)

    user = get_object_or_404(User, id=user_id)
    permission = Permission.objects.get(codename="can_view_gamekeeper_button")

    user.user_permissions.add(permission)

    # Clear the permission cache for the modified user
    if hasattr(user, '_perm_cache'):
        del user._perm_cache

    return redirect("EcoWorld:gamekeeper_page")



@permission_required("Accounts.can_view_gamekeeper_button")  # Only allowed gamekeeper can add challenges
def add_challenge(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            new_challenge = form.save(commit=False)  # Don't save to DB yet
            new_challenge.created_by = request.user  # Set creator manually
            new_challenge.save()  # Now save
            return redirect("EcoWorld:gamekeeper_page")  # Redirect back to the gamekeeper page after saving
    else:
        form = ChallengeForm()
    return render(request, "EcoWorld/add_challenge.html", {"form": form})




@login_required
def friends(request):
    """
    Web portal for friends in the ecoworld system. This page has 3 main parts: A current friends list, a search bar to add friends
    and a requests box.
    It uses the models created in accounts for friends and friend requests
    Depending on the action made it has returns for adding a friend in the search, accepting or declining a friend request and
    removing a friend from the friends list

    Author:
    Chris Lynch (cl1037@exeter.ac.uk)
    """
    if request.method == "GET":
        user=request.user
        userinfo = getUserInfo(request)

        #Gets pending requests
        friendreqs = FriendRequests.objects.filter(receiverID=user)

        userFriends = Friends.objects.filter(Q(userID1=user) | Q(userID2=user))



        return render(request, "EcoWorld/friends.html", {"userinfo" : userinfo[0], "friendreqs": friendreqs, "friends" : userFriends})

    elif request.method == "POST":
        userinfo = getUserInfo(request)
        user = request.user
        userID     = user.id
        #Gets pending requests
        friendreqs = FriendRequests.objects.filter(receiverID=user)

        #Gets user friends
        userFriends = Friends.objects.filter(Q(userID1=user) | Q(userID2=user))

        #Get the username sent in the form for adding friend
        username = request.POST.get("friendUsername")

        #Get friend request if sent and username
        friendAccOrRej = request.POST.get("friendar")
        friendAction = request.POST.get("friendaction")


        #Get removed friend if sent
        removeUser = request.POST.get("remove")


        #If the user is adding a friend
        if username:
            error = None
            #Gets the requested user for the friend request
            requestedUser = User.objects.filter(username=username).first()



            #Check for user existing
            if not requestedUser:
                error = "User Not Found!"
                return render(request, "EcoWorld/friends.html", {"userinfo": userinfo[0], "error" : error,"friendreqs" : friendreqs,"friends" : userFriends})

            #Check if user tried to add themselves
            if username == user.username:
                error = "You cant request yourself"
                return render(request, "EcoWorld/friends.html", {"userinfo": userinfo[0], "error" : error,"friendreqs" : friendreqs,"friends" : userFriends})

            requestedUserID = requestedUser.id
            existing_request = FriendRequests.objects.filter(senderID=userID, receiverID=requestedUserID).exists() or FriendRequests.objects.filter(senderID=requestedUserID, receiverID=userID).exists()

            #Checks if pending request already made
            if existing_request:
                error = "Friend request already pending"
                return render(request, "EcoWorld/friends.html", {"userinfo": userinfo[0], "error" : error,"friendreqs" : friendreqs,"friends" : userFriends})


            #Check if they are already friends
            existing_Friends = Friends.objects.filter(userID1=requestedUserID, userID2= userID).exists() or Friends.objects.filter(userID1=userID, userID2=requestedUserID).exists()
            if existing_Friends:
                error = "You are already friends with this user!"
                return render(request, "EcoWorld/friends.html", {"userinfo": userinfo[0], "error" : error,"friendreqs" : friendreqs,"friends" : userFriends})


            #Add request to database
            FriendRequests.objects.create(senderID=request.user, receiverID=requestedUser)
            AddMessage = "Friend request sent!"
            return render(request, "EcoWorld/friends.html", {"userinfo":userinfo[0],"friendreqs" : friendreqs, "addmessage": AddMessage,"friends" : userFriends})

        #If the user is accepting or rejecting a friend request
        elif friendAccOrRej:
            #Gets requested user for DB
            requestedUser = User.objects.filter(username=friendAccOrRej).first()

            #If accepted friend request
            if friendAction == "accept":
                #Creates row in friends table and removes from requests
                Friends.objects.create(userID1=user, userID2=requestedUser)
                FriendRequests.objects.filter(senderID=requestedUser, receiverID=user).delete()

                #Gets active requests and friends again to return
                friendreqs = FriendRequests.objects.filter(receiverID=user)
                userFriends = Friends.objects.filter(Q(userID1=user) | Q(userID2=user))

                return render(request, "EcoWorld/friends.html", {"userinfo":userinfo[0],"friendreqs" : friendreqs,"friends" : userFriends})

            else:
                #Deletes friend request info as its a reject
                FriendRequests.objects.filter(senderID=requestedUser, receiverID=user).delete()

                #Updates data on friend requests
                friendreqs = FriendRequests.objects.filter(receiverID=user)

                return render(request, "EcoWorld/friends.html", {"userinfo":userinfo[0],"friendreqs" : friendreqs,"friends" : userFriends})





        #If removing a friend
        else:
            removeUser = User.objects.filter(username=removeUser).first()
            removeUserID = removeUser.id
            Friends.objects.filter(Q(userID1=user, userID2=removeUserID) | Q(userID1=removeUserID, userID2=user)).delete()

            #Updates data on friend requests
            friendreqs = FriendRequests.objects.filter(receiverID=user)



            return render(request, "EcoWorld/friends.html", {"userinfo":userinfo[0],"friendreqs" : friendreqs,"friends" : userFriends})


def mergecards(request):
    user = request.user
    userinfo = getUserInfo(request)

    if request.method == "GET":

        merge, created = Merge.objects.get_or_create(userID=request.user)

        cardImages = []

        #Go through the merge DB and get the mergeCardID and the image for the template
        for i in range(1, 6):
            cardField = getattr(merge, f'cardID{i}', None)
            if cardField:
                cardImages.append({'id': f'cardID{i}', 'image': cardField.image.url})
            else:
                cardImages.append({'id': None, 'image' : None})



        return render(request, "EcoWorld/mergecards.html", {"userinfo" : userinfo[0], "merge":cardImages})

    elif request.method == "POST":
        #Gets rarity option chosen if so
        rarity = request.POST.get("rarity")
        addCard = request.POST.get("addCard")
        removeCard = request.POST.get("removeCard")

        mergeCardsFunc = request.POST.get("mergebutton")



        if rarity:
            #Gets the player inventory for the certain rarity
            playerInventoryStorage = ownsCard.objects.filter(user=request.user, card__rarity_id=rarity).select_related('card').values('card__title', 'card__image', 'quantity', 'card__id')

            #Puts the media tag onto the image for it to be used
            for item in playerInventoryStorage:
                item['card__image'] = "/media/" + item['card__image']


            playerItems = playerInventoryStorage

            merge, created = Merge.objects.get_or_create(userID=request.user)

            cardImages = []

            #Go through the merge DB and get the mergeCardID and the image for the template
            for i in range(1, 6):
                cardField = getattr(merge, f'cardID{i}', None)
                if cardField:
                    cardImages.append({'id': f'cardID{i}', 'image': cardField.image.url})
                else:
                    cardImages.append({'id': None, 'image' : None})


            return render(request, "EcoWorld/mergecards.html", {"userinfo" : userinfo[0], "playerItems": playerItems, "rarity":rarity,"merge":cardImages},)

        if addCard:
            #Get rarity and card id
            rarityforbutton = request.POST.get("rarityforbutton")
            cardID = addCard

            merge, created = Merge.objects.get_or_create(userID=request.user)

            cardImages = []

            #Go through the merge DB and get the mergeCardID and the image for the template
            for i in range(1, 6):
                cardField = getattr(merge, f'cardID{i}', None)
                if cardField:
                    cardImages.append({'id': f'cardID{i}', 'image': cardField.image.url})
                else:
                    cardImages.append({'id': None, 'image' : None})

            #Gets the player inventory for the certain rarity
            playerInventoryStorage = ownsCard.objects.filter(user=request.user, card__rarity_id=rarityforbutton).select_related('card').values('card__title', 'card__image', 'quantity', 'card__id')

            #Puts the media tag onto the image for it to be used
            for item in playerInventoryStorage:
                item['card__image'] = "/media/" + item['card__image']


            playerItems = playerInventoryStorage

            error = None
            merge, created = Merge.objects.get_or_create(userID=request.user)

            if merge and (merge.cardID1 and merge.cardID2 and merge.cardID3 and merge.cardID4 and merge.cardID5):
                error = "There are already 5 cards in the merge slots remove one first!"
                return render(request, "EcoWorld/mergecards.html", {"userinfo" : userinfo[0], "playerItems": playerItems, "rarity": rarityforbutton, "error" : error,"merge":cardImages})

            cardToAdd = card.objects.get(id=cardID)  # Get the card object by ID
            cardRarityID = cardToAdd.rarity.id  # Access the rarity of the card
            ownCard = ownsCard.objects.get(user=request.user, card_id=cardID) #Amount owned of the card to be used with quantity


            if merge.cardID1:
                firstCard = merge.cardID1
                if firstCard.rarity_id != cardRarityID:
                    error = "The card you tried to add was not of the same rarity as the first card in the merge."
                    return render(request, "EcoWorld/mergecards.html", {"userinfo": userinfo[0], "playerItems": playerItems, "rarity": rarityforbutton, "error": error,"merge":cardImages})


            if ownCard.quantity <= 0:
                error = "You need to get more of this card to add it to the merge or take one out of the merge box"
                return render(request, "EcoWorld/mergecards.html", {"userinfo" : userinfo[0], "playerItems": playerItems, "rarity": rarityforbutton, "error" : error,"merge":cardImages})


            if merge:
                # Check for available slot to add the card
                if not merge.cardID1:
                    merge.cardID1 = cardToAdd
                elif not merge.cardID2:
                    merge.cardID2 = cardToAdd
                elif not merge.cardID3:
                    merge.cardID3 = cardToAdd
                elif not merge.cardID4:
                    merge.cardID4 = cardToAdd
                elif not merge.cardID5:
                    merge.cardID5 = cardToAdd
                merge.save()

            ownCard.quantity -=1
            ownCard.save()

            #Gets the player inventory for the certain rarity
            playerInventoryStorage = ownsCard.objects.filter(user=request.user, card__rarity_id=rarityforbutton).select_related('card').values('card__title', 'card__image', 'quantity', 'card__id')

            #Puts the media tag onto the image for it to be used
            for item in playerInventoryStorage:
                item['card__image'] = "/media/" + item['card__image']

            # Filter items where quantity is greater than 0
            playerItems = playerInventoryStorage

            merge, created = Merge.objects.get_or_create(userID=request.user)

            cardImages = []

            #Go through the merge DB and get the mergeCardID and the image for the template
            for i in range(1, 6):
                cardField = getattr(merge, f'cardID{i}', None)
                if cardField:
                    cardImages.append({'id': f'cardID{i}', 'image': cardField.image.url})
                else:
                    cardImages.append({'id': None, 'image' : None})

            return render(request, "EcoWorld/mergecards.html", {"userinfo" : userinfo[0], "playerItems": playerItems, "rarity": rarityforbutton,"merge":cardImages})

        if removeCard:
            #Get rarity and card id
            rarityforbutton = request.POST.get("rarityforbutton")
            cardID = removeCard

            #Gets the player inventory for the certain rarity
            playerInventoryStorage = ownsCard.objects.filter(user=request.user, card__rarity_id=rarityforbutton).select_related('card').values('card__title', 'card__image', 'quantity', 'card__id')

            #Puts the media tag onto the image for it to be used
            for item in playerInventoryStorage:
                item['card__image'] = "/media/" + item['card__image']


            playerItems = playerInventoryStorage

            error = None
            merge, created = Merge.objects.get_or_create(userID=request.user)

            cardToRemove = None
            if merge.cardID1 and str(merge.cardID1.id) == str(cardID):
                cardToRemove = merge.cardID1
                merge.cardID1 = None
            elif merge.cardID2 and str(merge.cardID2.id) == str(cardID):
                cardToRemove = merge.cardID2
                merge.cardID2 = None
            elif merge.cardID3 and str(merge.cardID3.id) == str(cardID):
                cardToRemove = merge.cardID3
                merge.cardID3 = None
            elif merge.cardID4 and str(merge.cardID4.id) == str(cardID):
                cardToRemove = merge.cardID4
                merge.cardID4 = None
            elif merge.cardID5 and str(merge.cardID5.id) == str(cardID):
                cardToRemove = merge.cardID5
                merge.cardID5 = None

            if cardToRemove:
                # Update the user's inventory by adding 1 back
                ownCard = ownsCard.objects.get(user=request.user, card_id=cardID)
                ownCard.quantity += 1

                #Save merge db and ownsCard db for user
                ownCard.save()
                merge.save()


                #Gets the player inventory for the certain rarity
                playerInventoryStorage = ownsCard.objects.filter(user=request.user, card__rarity_id=rarityforbutton).select_related('card').values('card__title', 'card__image', 'quantity', 'card__id')

                #Puts the media tag onto the image for it to be used
                for item in playerInventoryStorage:
                    item['card__image'] = "/media/" + item['card__image']


                playerItems = playerInventoryStorage

                merge, created = Merge.objects.get_or_create(userID=request.user)

                cardImages = []

                #Go through the merge DB and get the mergeCardID and the image for the template
                for i in range(1, 6):
                    cardField = getattr(merge, f'cardID{i}', None)
                    if cardField:
                        cardImages.append({'id': f'cardID{i}', 'image': cardField.image.url})
                    else:
                        cardImages.append({'id': None, 'image' : None})


                return render(request, "EcoWorld/mergecards.html", {"userinfo" : userinfo[0], "playerItems": playerItems, "rarity": rarityforbutton,"merge":cardImages})

            else:
                merge, created = Merge.objects.get_or_create(userID=request.user)

                cardImages = []

                #Go through the merge DB and get the mergeCardID and the image for the template
                for i in range(1, 6):
                    cardField = getattr(merge, f'cardID{i}', None)
                    if cardField:
                        cardImages.append({'id': f'cardID{i}', 'image': cardField.image.url})
                    else:
                        cardImages.append({'id': None, 'image' : None})
                error = "This card is not in a merge slot"
                return render(request, "EcoWorld/mergecards.html", {"userinfo" : userinfo[0], "playerItems": playerItems, "rarity": rarityforbutton, "error" : error,"merge":cardImages})



        if mergeCardsFunc:
            #Gets the player inventory for the certain rarity
            playerInventoryStorage = ownsCard.objects.filter(user=request.user, card__rarity_id=rarity).select_related('card').values('card__title', 'card__image', 'quantity', 'card__id')

            #Puts the media tag onto the image for it to be used
            for item in playerInventoryStorage:
                item['card__image'] = "/media/" + item['card__image']


            playerItems = playerInventoryStorage

            merge, created = Merge.objects.get_or_create(userID=request.user)

            rarity = mergeCardsFunc

            cardImages = []

            #Go through the merge DB and get the mergeCardID and the image for the template
            for i in range(1, 6):
                cardField = getattr(merge, f'cardID{i}', None)
                if cardField:
                    cardImages.append({'id': f'cardID{i}', 'image': cardField.image.url})
                else:
                    cardImages.append({'id': None, 'image' : None})


            if mergeCardsFunc == 5:
                error = "This card rarity cannot be merged!"
                return render(request, "EcoWorld/mergecards.html", {"userinfo" : userinfo[0], "playerItems": playerItems, "rarity":rarity,"merge":cardImages, "error":error},)


            if merge.cardID1 and merge.cardID2 and merge.cardID3 and merge.cardID4 and merge.cardID5:
                merge.cardID1 = None
                merge.cardID2 = None
                merge.cardID3 = None
                merge.cardID4 = None
                merge.cardID5 = None



                mergeCardsFunc = int(mergeCardsFunc)
                mergeCardsFunc += 1

                cards = card.objects.filter(rarity=mergeCardsFunc)
                cardToReturn = random.choice(cards)

                cardImage = cardToReturn.image.url

                userCard, created = ownsCard.objects.get_or_create(user=request.user, card=cardToReturn)

                # If the card already exists in the user's inventory, increment the quantity
                if not created:
                    userCard.quantity += 1
                    userCard.save()
                else:
                    # If the card is newly added to the inventory, set quantity to 1
                    userCard.quantity = 1
                    userCard.save()
                merge.save()

                merge, created = Merge.objects.get_or_create(userID=request.user)



                cardImages = []

                #Go through the merge DB and get the mergeCardID and the image for the template
                for i in range(1, 6):
                    cardField = getattr(merge, f'cardID{i}', None)
                    if cardField:
                        cardImages.append({'id': f'cardID{i}', 'image': cardField.image.url})
                    else:
                        cardImages.append({'id': f'cardID{i}', 'image' : None})


                return render(request, "EcoWorld/merge_opening_page.html", {"image": cardToReturn.image.url})


        return render(request, "EcoWorld/mergecards.html", {"userinfo" : userinfo[0]})


def merge_opening_page(request):
    return render(request, "EcoWorld/merge_opening_page.html")


@csrf_exempt
@login_required
def save_objective_note(request):
    if request.method == "POST":
        data = json.loads(request.body)
        objective_id = data.get("objective_id")
        message = data.get("message")

        try:
            objective = ongoingChallenge.objects.get(id=objective_id, user=request.user)
            objective.submission = message  # Store the user's note
            objective.save()
            Post.create_from_ongoing_challenge(objective)
            return JsonResponse({"success": True})
        except ongoingChallenge.DoesNotExist:
            return JsonResponse({"error": "Objective not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)