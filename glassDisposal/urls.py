from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_disposal, name='submit_disposal'), #URL for submitting glass disposal
    path('thankyou/', views.thankyou, name='thankyou')
]