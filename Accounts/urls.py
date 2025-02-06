from django.urls import path
from .views import dbTest,signUpView  # Import the view

urlpatterns = [
    path('', dbTest, name='home'),  # Root URL
    path('signup/', signUpView, name='signup'),  # URL for the signup page
]