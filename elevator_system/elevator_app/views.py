from django.shortcuts import render
from django.http import JsonResponse
from .models import Elevator, FloorRequest
from .controller import ElevatorSystemController

# Initialize the elevator system with 5 elevators
elevator_system = ElevatorSystemController(5)

def initialize_elevator_system(request):
    """Initialize the elevator system with a given number of elevators."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    num_elevators = request.POST.get('num_elevators')
    if not num_elevators:
        return JsonResponse({'error': 'Number of elevators not provided'}, status=400)

    # Initialize the elevator system with the given number of elevators
    elevator_system.__init__(num_elevators)

    return JsonResponse({'success': 'Elevator system initialized'}, status=200)

def get_requests_for_elevator(request, elevator_id):
    """Get all requests for a given elevator."""
    elevator = Elevator.objects.get(pk=elevator_id)
    requests = elevator.requests.all()

    request_data = []
    for request in requests:
        data = {
            'id': request.id,
            'floor': request.floor,
            'direction': request.direction,
        }
        request_data.append(data)

    return JsonResponse({'requests': request_data}, status=200)

def get_next_destination_for_elevator(request, elevator_id):
    """Get the next destination floor for a given elevator."""
    elevator = Elevator.objects.get(pk=elevator_id)
    if not elevator.requests.exists():
        return JsonResponse({'error': 'No requests for this elevator'}, status=404)

    next_request = elevator.requests.first()
    return JsonResponse({'next_destination': next_request.floor}, status=200)

def get_elevator_movement(request, elevator_id):
    """Get if the elevator is moving up or down currently."""
    elevator = Elevator.objects.get(pk=elevator_id)
    return JsonResponse({'movement': elevator.movement}, status=200)

