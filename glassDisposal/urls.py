from django.urls import path
from .views import submit_disposal, thankyou

urlpatterns = [
    path('submit/', submit_disposal, name='submit_disposal'),
    path('thankyou/<int:coins_earned>/', thankyou, name='thankyou'),
]
