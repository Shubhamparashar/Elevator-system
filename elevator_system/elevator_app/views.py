from django.shortcuts import render
from django.http import JsonResponse
from .models import Elevator, FloorRequest
from .controller import ElevatorSystemController
from django.views.decorators.csrf import csrf_exempt, method_decorator


# Initialize the elevator system with 5 elevators
elevator_system = ElevatorSystemController(5)

@method_decorator(csrf_exempt, name='dispatch')
def initialize_elevator_system(request):
    """Initialize the elevator system with a given number of elevators."""
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request method'}, status=405)

        num_elevators = int(request.POST.get('num_elevators'))
        if not num_elevators:
            return JsonResponse({'error': 'Number of elevators not provided'}, status=400)
        num_floors = int(request.POST.get('num_floors', 0))
        # Initialize the elevator system with the given number of elevators
        if num_floors: 
            elevator_system.__init__(num_elevators, num_floors)
        else: 
            elevator_system.__init__(num_elevators)
        return JsonResponse({'success': 'Elevator system initialized'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_requests_for_elevator(request, elevator_id):
    """Get all requests for a given elevator."""
    try:

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
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def get_next_destination_for_elevator(request, elevator_id):
    """Get the next destination floor for a given elevator."""
    try:
        elevator = Elevator.objects.get(pk=elevator_id)
        
        if not elevator.requests.exists():
            return JsonResponse({'error': 'No requests for this elevator'}, status=404)

        next_request = elevator.requests.first()
        return JsonResponse({'next_destination': next_request.floor}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_elevator_movement(request, elevator_id):
    """Get if the elevator is moving up or down currently."""
    try:
        elevator = Elevator.objects.get(pk=elevator_id)
        return JsonResponse({'movement': elevator.movement}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def save_user_request(request):
    """Save a user request to the list of requests for an elevator."""
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request method'}, status=405)

        floor = request.POST.get('floor')
        direction = request.POST.get('direction')
        if not floor or not direction:
            return JsonResponse({'error': 'Floor and direction must be provided'},status=400)
     # Call the elevator system to handle the request
        elevator_system.handle_request(floor, direction)
        return JsonResponse({'success': 'Request added to elevator queue'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def mark_elevator_as_not_working(request, elevator_id):
    """Mark an elevator as not working or in maintenance."""
    elevator = Elevator.objects.get(pk=elevator_id)
    elevator.is_working = False
    elevator.save()

    return JsonResponse({'success': 'Elevator marked as not working'}, status=200)

def set_door_status(request, elevator_id):
    """Set the door status of an elevator."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    status = request.POST.get('status')
    if not status:
        return JsonResponse({'error': 'Door status must be provided'}, status=400)
    elevator = Elevator.objects.get(pk=elevator_id)
    elevator.door_status = status
    elevator.save()

    return JsonResponse({'success': 'Door status set'}, status=200)

def get_elevator_status(request, elevator_id):
    """Get the current status of an elevator."""
    elevator = Elevator.objects.get(pk=elevator_id)
    status = {
        'current_floor': elevator.current_floor,
        'movement': elevator.movement,
        'door_status': elevator.door_status,
        'is_working': elevator.is_working,
    }
    return JsonResponse({'status': status}, status=200)

def get_elevator_list(request):
    """Get a list of all elevators in the system."""
    elevators = Elevator.objects.all()

    elevator_list = []
    for elevator in elevators:
        data = {
            'id': elevator.id,
            'current_floor': elevator.current_floor,
            'movement': elevator.movement,
            'door_status': elevator.door_status,
            'is_working': elevator.is_working,
            'num_requests': elevator.requests.count(),
        }
        elevator_list.append(data)

    return JsonResponse({'elevators': elevator_list}, status=200)

def get_request_list(request):
    """Get a list of all requests in the system."""
    requests = FloorRequest.objects.all()

    request_list = []
    for request in requests:
        data = {
            'id': request.id,
            'elevator': request.elevator.id,
            'floor': request.floor,
            'direction': request.direction,
        }
        request_list.append(data)

    return JsonResponse({'requests': request_list}, status=200)

def cancel_request(request, request_id):
    """Cancel a request made by a user."""
    floor_request = FloorRequest.objects.get(pk=request_id)
    floor_request.delete()

    elevator = floor_request.elevator
    elevator.update_request_list()

    return JsonResponse({'success': 'Request cancelled'}, status=200)

def emergency_stop(request, elevator_id):
    """Immediately stop an elevator in case of an emergency."""
    elevator = Elevator.objects.get(pk=elevator_id)
    elevator.movement = 'stopped'
    elevator.door_status = 'open'
    elevator.save()

    return JsonResponse({'success': 'Elevator stopped'}, status=200)

