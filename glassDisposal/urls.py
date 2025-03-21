from django.urls import path
from .views import submit_disposal, thankyou, add_recycling_point, delete_recycling_point

urlpatterns = [
    path('submit/', submit_disposal, name='submit_disposal'),
    path('thankyou/<int:coins_earned>/', thankyou, name='thankyou'),
    path('add_recycling_point/', add_recycling_point, name='add_recycling_point'),
    path('delete_recycling_point/',
         delete_recycling_point,
         name='delete_recycling_point_list'),  # List view
    path('delete_recycling_point/<int:pk>/',
         delete_recycling_point,
         name='delete_recycling_point'),  # Delete detail view
]