from django.shortcuts import render

# Create your views here.
def chest(request):
    return render(request, "chest.html")