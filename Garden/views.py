from django.shortcuts import render
from .models import garden
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
    return render(request, 'Garden/garden.html', {'squares': processedSquares,'MEDIA_URL':settings.MEDIA_URL})