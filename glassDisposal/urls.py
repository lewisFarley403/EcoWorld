"""
URL configuration for the glassDisposal app.

Defines routing for submitting a glass disposal entry and displaying the thank-you page.

Routes:
    /submit/ – Handles the glass disposal form submission.
    /thankyou/<int:coins_earned>/ – Displays the thank-you page with coins awarded.

Author:
    Charlie Shortman
"""

from django.urls import path
from .views import submit_disposal, thankyou

# URL patterns for the glass disposal feature
urlpatterns = [
    path('submit/', submit_disposal, name='submit_disposal'),  # Form for submitting a disposal
    path('thankyou/<int:coins_earned>/', thankyou, name='thankyou'),  # Page showing coins earned
]
