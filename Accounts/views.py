from django.shortcuts import render
from .models import User
from .forms import UserForm
# Create your views here.
def dbTest(request):
    users = User.objects.all()
    print(list(users))
    return render(request, "dbTest.html", {"users": users})

def signUpView(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserForm()
    return render(request, "signup.html", {"form": form})