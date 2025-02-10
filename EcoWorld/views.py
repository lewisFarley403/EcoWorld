"""
this module defines the views used in this app:
    - `addDrink` : This view allows the user to add a drink event
    - `testAddDrink` : This view allows the user to test adding a drink event (for testing purposes)
Author:
    -Lewis Farley (lf507@exeter.ac.uk)
"""

from django.shortcuts import render
from .models import drinkEvent,User,waterFountain
import json
from django.http import HttpResponse
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