from django.urls import path
from . import views

urlpatterns = [

    path('initialize_elevator_system/', views.initialize_elevator_system, name='initialize_elevator_system'),
    path('fetch_all_requests/<int:elevator_id>', views.get_requests_for_elevator, name='fetch_all_requests'),
    path('fetch_next_destination/<int:elevator_id>', views.get_next_destination_for_elevator, name='fetch_next_destination'),
    path('fetch_elevator_movement/<int:elevator_id>', views.get_elevator_movement, name='fetch_elevator_movement'),
    path('save_user_request/', views.save_user_request, name='save_user_request')
]