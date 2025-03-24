"""
this module defines the views used in this app:
    - `addDrink` : This view allows the user to add a drink event
    - `testAddDrink` : This view allows the user to test adding a drink event (for testing purposes)
Author:
    -Lewis Farley (lf507@exeter.ac.uk)
    -Chris Lynch (cl1037@exeter.ac.uk)
"""
import json
import random
from datetime import date
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from Accounts.models import Friends, FriendRequests
from forum.models import Post, PostInteraction
from qrCodes.models import drinkEvent
from .forms import ChallengeForm
from .models import User, pack, ownsCard, ongoingChallenge, card, Merge
from .utils import getUsersChallenges


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

    #Upon loading the page the dashboard needs its username and pfp along with coins,
    # this function here gives it to the dashboard html file
    if request.method == "GET":
        userinfo = getUserInfo(request)

        return render(request, "EcoWorld/dashboard.html", {"userinfo":userinfo[0]})

@login_required
def store(request):
    """
    This view renders the store for the ecoworld page.
    This pages purpose is to allow users to purchase packs to unlock cards with their coins
    It requires the user to be logged in
    Returns:
    Render request plus two dictionaries one of user data for the header
    and one of the pack data for viewing

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
        return render(request, "EcoWorld/store.html",{ "packs": pack_list, "userinfo": userinfo[0]})

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
    Webpage to render the pack opening animation. When a pack is bought it
    redirects to here where it will send the correct info
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
    """
    Renders the Challenges page for the logged-in user,
    showing active daily objectives and tracking drinking cooldown.

    - Fetches all current ongoing challenges (daily objectives) for the user.
    - Checks the user's last drink time to determine drink button availability.
    - Calculates completed and total challenge progress.
    - Passes context data such as coins, cooldown, and challenge progress to the template.

    Returns:
        HttpResponse: Renders the 'challenge_page.html' template with user-specific challenge data.

    Author:
        Lewis Farley (lf507@exeter.ac.uk), Theodore Armes (tesa201@exeter.ac.uk)
    """
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
    # Total worth of all objectives
    total_objective_worth = sum(obj.challenge.goal for obj in daily_objectives)
    # Sum of completed progress
    completed_objective_worth = sum(obj.progress for obj in daily_objectives)
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
    Increments the progress of a daily objective by 1 and rewards coins when completed.

    - Retrieves the objective ID from the POST request.
    - Increases the progress counter if it hasn't reached the goal.
    - Marks the objective as completed and rewards the user with coins if fully completed.
    - Returns updated progress and total completion data.

    Returns:
        JsonResponse: Contains success status, progress updates, and reward information.

    Author:
        Lewis Farley (lf507@exeter.ac.uk), Theodore Armes (tesa201@exeter.ac.uk)
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


            users_ongoing_challenges = ongoingChallenge.objects.filter(user=request.user)
            completed_objectives_count =0
            for challenge in users_ongoing_challenges:
                if challenge.is_complete():
                    completed_objectives_count +=1

            daily_objectives = getUsersChallenges(request.user)
            # Total worth of all objectives
            total_objective_worth = sum(obj.challenge.goal for obj in daily_objectives)

            # Sum of completed progress
            completed_objective_worth = sum(obj.progress for obj in daily_objectives)
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
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

@login_required
def completeChallenge(request):
    """
    Marks a challenge as completed for the logged-in user and updates their reward.

    - Retrieves the challenge ID from the POST request.
    - Updates the user's profile by adding reward coins.
    - Sets the completion timestamp for the challenge.
    - Saves the updated challenge status in the database.

    Returns:
        HttpResponse: Success or failure message.

    Author:
        Lewis Farley (lf507@exeter.ac.uk), Theodore Armes (tesa201@exeter.ac.uk)
    """
    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(id=request.user.id)
        on_going_challenge = data["id"]

        chal = ongoingChallenge.objects.get(id=on_going_challenge)
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
    This view renders the gamekeeper page, which allows gamekeepers 
    to do things a regular user cannot.
    Returns: render request and a list of users who are not gamekeepers

    Author:
        Ethan Sweeney (es1052@exeter.ac.uk)
    """
    if request.method == "GET":
        userinfo = getUserInfo(request)

    users = User.objects.exclude(user_permissions__codename="can_view_gamekeeper_button")
    missing_rows = range(max(0, 3 - users.count()))

    # Get forum posts data
    posts = Post.objects.all().order_by('-created_at')
    posts_data = []
    for post in posts:
        likes = PostInteraction.objects.filter(post=post, interaction_type='like').count()
        dislikes = PostInteraction.objects.filter(post=post, interaction_type='dislike').count()
        ratio = f"{dislikes/(likes + dislikes):.2%}" if (likes + dislikes) > 0 else "N/A"
        posts_data.append({
            'post': post,
            'likes': likes,
            'dislikes': dislikes,
            'ratio': ratio
        })

    return render(request, "EcoWorld/gamekeeper_page.html", {
        "users": users, 
        "missing_rows": missing_rows, 
        "userinfo": userinfo[0],
        "posts": posts_data
    })

@permission_required("Accounts.can_view_gamekeeper_button")  # Only gamekeepers can promote others
def grant_gamekeeper(request, user_id):
    """
    This view grants the can_view_gamekeeper_button permission to a user,
    effectively promoting them to an gamekeeper.

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
    """
    This view allows gamekeepers to add challenges to the system.

    Returns: Render request and a form to add a challenge.

    Author:
        Ethan Sweeney (es1052@exeter.ac.uk)
    """
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            new_challenge = form.save(commit=False)  # Don't save to DB yet
            new_challenge.created_by = request.user  # Set creator manually
            new_challenge.save()  # Now save
            # Redirect back to the gamekeeper page after saving
            return redirect("EcoWorld:gamekeeper_page")
    else:
        form = ChallengeForm()
    return render(request, "EcoWorld/add_challenge.html", {"form": form})

def friends(request):
    """
    Web portal for friends in the ecoworld system. This page has 2 main parts:
    - A current friends list
    - a search bar to add friends
    and a requests box.
    It uses the models created in accounts for friends and friend requests
    Depending on the action made it has returns for adding a friend in the search,
    accepting or declining a friend request and
    removing a friend from the friends list

    Author:
        Chris Lynch (cl1037@exeter.ac.uk)
    """
    if request.method == "GET":
        user=request.user
        userinfo = getUserInfo(request)

        #Gets pending requests
        friendreqs = FriendRequests.objects.filter(receiverID=user)

        user_friends = Friends.objects.filter(Q(userID1=user) | Q(userID2=user))



        return render(request, "EcoWorld/friends.html",
                      {"userinfo" : userinfo[0],
                       "friendreqs": friendreqs,
                       "friends" : user_friends})

    elif request.method == "POST":
        userinfo = getUserInfo(request)
        user = request.user
        user_id= user.id
        #Gets pending requests
        friendreqs = FriendRequests.objects.filter(receiverID=user)

        #Gets user friends
        user_friends = Friends.objects.filter(Q(userID1=user) | Q(userID2=user))

        #Get the username sent in the form for adding friend
        username = request.POST.get("friendUsername")

        #Get friend request if sent and username
        friend_acc_or_rej = request.POST.get("friendar")
        friend_action = request.POST.get("friendaction")


        #Get removed friend if sent
        remove_user = request.POST.get("remove")


        #If the user is adding a friend
        if username:
            error = None
            #Gets the requested user for the friend request
            requested_user = User.objects.filter(username=username).first()



            #Check for user existing
            if not requested_user:
                error = "User Not Found!"
                return render(request, "EcoWorld/friends.html",
                              {"userinfo": userinfo[0],
                               "error" : error,
                               "friendreqs" : friendreqs,
                               "friends" : user_friends})

            #Check if user tried to add themselves
            if username == user.username:
                error = "You cant request yourself"
                return render(request, "EcoWorld/friends.html",
                              {"userinfo": userinfo[0],
                               "error" : error,
                               "friendreqs" : friendreqs,
                               "friends" : user_friends})

            requested_user_id = requested_user.id
            f1 = FriendRequests.objects.filter(senderID=user_id,
                                               receiverID=requested_user_id).exists()
            f2 = FriendRequests.objects.filter(senderID=requested_user_id,
                                               receiverID=user_id).exists()
            existing_request = f1 or f2

            #Checks if pending request already made
            if existing_request:
                error = "Friend request already pending"
                return render(request, "EcoWorld/friends.html",
                              {"userinfo": userinfo[0],
                               "error" : error,
                               "friendreqs" : friendreqs,
                               "friends" : user_friends})


            #Check if they are already friends
            f1 =Friends.objects.filter(userID1=user_id, userID2=requested_user_id).exists()
            f2= Friends.objects.filter(userID1=requested_user_id, userID2= user_id).exists()
            existing_friends =  f2 or f1
            if existing_friends:
                error = "You are already friends with this user!"
                return render(request, "EcoWorld/friends.html",
                              {"userinfo": userinfo[0],
                               "error" : error,
                               "friendreqs" : friendreqs,
                               "friends" : user_friends})


            #Add request to database
            FriendRequests.objects.create(senderID=request.user, receiverID=requested_user)
            add_message = "Friend request sent!"
            return render(request, "EcoWorld/friends.html",
                          {"userinfo":userinfo[0],
                           "friendreqs" : friendreqs,
                           "addmessage": add_message,
                           "friends" : user_friends})

        #If the user is accepting or rejecting a friend request
        elif friend_acc_or_rej:
            #Gets requested user for DB
            requested_user = User.objects.filter(username=friend_acc_or_rej).first()

            #If accepted friend request
            if friend_action == "accept":
                #Creates row in friends table and removes from requests
                Friends.objects.create(userID1=user, userID2=requested_user)
                FriendRequests.objects.filter(senderID=requested_user, receiverID=user).delete()

                #Gets active requests and friends again to return
                friendreqs = FriendRequests.objects.filter(receiverID=user)
                user_friends = Friends.objects.filter(Q(userID1=user) | Q(userID2=user))

                return render(request, "EcoWorld/friends.html",
                              {"userinfo":userinfo[0],
                               "friendreqs" : friendreqs,
                               "friends" : user_friends})

            else:
                #Deletes friend request info as its a reject
                FriendRequests.objects.filter(senderID=requested_user, receiverID=user).delete()

                #Updates data on friend requests
                friendreqs = FriendRequests.objects.filter(receiverID=user)

                return render(request, "EcoWorld/friends.html",
                              {"userinfo":userinfo[0],
                               "friendreqs" : friendreqs,
                               "friends" : user_friends})





        #If removing a friend
        else:
            remove_user = User.objects.filter(username=remove_user).first()
            if remove_user:
                remove_user_id = remove_user.id
                Friends.objects.filter(Q(userID1=user, userID2=remove_user_id) | Q(userID1=remove_user_id, userID2=user)).delete()

            #Updates data on friend requests
            friendreqs = FriendRequests.objects.filter(receiverID=user)



            return render(request, "EcoWorld/friends.html",
                          {"userinfo":userinfo[0],
                           "friendreqs" : friendreqs,
                           "friends" : user_friends})



@login_required
def mergecards(request):
    """
    Function to handle all the intricacies of merging cards together.
    It allows users to add and remove cards from the slots in their individual merge area
    It allows users to merge 5 cards of the same rarity together
    It renders the page for each POST request to keep updating entries
    This function uses the merge model in models.py to hold cards entered into the merge slots
    
    Author: 
    Chris Lynch (cl1037@exeter.ac.uk)
    """
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



        return render(request, "EcoWorld/mergecards.html",
                      {"userinfo" : userinfo[0],
                       "merge":cardImages})

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


            try:
                if int(mergeCardsFunc) == 5:
                    error = "This card rarity cannot be merged!"
                    return render(request, "EcoWorld/mergecards.html",
                                  {"userinfo": userinfo[0], "playerItems": playerItems, "rarity": rarity,
                                   "merge": cardImages, "error": error})
            except TypeError:
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
                return render(request, "EcoWorld/mergecards.html", {"userinfo" : userinfo[0], "playerItems": playerItems, "rarity":rarity,"merge":cardImages, "error":error})


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
    """
    Saves a user-provided note upon completing a daily objective.

    - Expects a POST request with `objective_id` and `message` in the JSON payload.
    - Updates the submission field of the corresponding ongoing challenge.
    - Saves the updated challenge object.

    Returns:
        JsonResponse: Success or failure status.

    Author:
        Theodore Armes (tesa201@exeter.ac.uk)
    """
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