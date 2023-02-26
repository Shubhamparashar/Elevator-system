from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (ElevatorActionViewSet, ElevatorMovementViewSet, UserRequestViewSet, SetElevatorStatusView, ElevatorViewSet, FloorRequestViewSet)

router = DefaultRouter()
router.register(r'action', ElevatorActionViewSet, basename='action')
router.register(r'movement', ElevatorMovementViewSet, basename='movement')
router.register(r'user-request', UserRequestViewSet, basename='user_request')
router.register(r'set-elevator-status', SetElevatorStatusView, basename='set_elevator_status')
router.register(r'details', ElevatorViewSet, basename='details')
router.register(r'floor-requests', FloorRequestViewSet, basename='floorrequest')


urlpatterns = [
    path('', include(router.urls)),
]