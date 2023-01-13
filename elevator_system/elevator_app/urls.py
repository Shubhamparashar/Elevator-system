from django.urls import path
from . import views

urlpatterns = [

    path('initialize_elevator_system/', views.initialize_elevator_system, name='initialize_elevator_system'),
    path('fetch_all_requests/<int:elevator_id>', views.get_requests_for_elevator, name='fetch_all_requests'),
    path('fetch_next_destination/<int:elevator_id>', views.get_next_destination_for_elevator, name='fetch_next_destination'),
    path('fetch_elevator_movement/<int:elevator_id>', views.get_elevator_movement, name='fetch_elevator_movement'),
    path('save_user_request/', views.save_user_request, name='save_user_request'),
    path('move_current_elevator/', views.request_to_move_current_elevator, name='move_current_elevator'),
    path('mark_elevator_as_not_working/', views.mark_elevator_as_not_working, name='mark_elevator_as_not_working'),
    path('set_door_status/<int:elevator_id>', views.set_door_status, name='set_door_status'),
    path('get_elevator_status/<int:elevator_id>', views.get_elevator_status, name='get_elevator_status'),
    path('get_elevator_list/', views.get_elevator_list, name='get_elevator_list'),
    path('get_request_list/', views.get_request_list, name='get_request_list'),
    path('emergency_stop/<int:elevator_id>', views.emergency_stop, name='emergency_stop'),
]