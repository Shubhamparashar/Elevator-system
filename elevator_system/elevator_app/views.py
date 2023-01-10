from django.http import JsonResponse
from .models import Elevator, FloorRequest
from .controller import ElevatorSystemController
from django.views.decorators.csrf import csrf_exempt


# Initialize the elevator system with 5 elevators
elevator_system = ElevatorSystemController(5)

@csrf_exempt
def initialize_elevator_system(request):
    """Initialize the elevator system with a given number of elevators."""
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request method'}, status=405)

        num_elevators = int(request.POST.get('num_elevators'))
        if not num_elevators:
            return JsonResponse({'error': 'Number of elevators not provided'}, status=400)

        # Initialize the elevator system with the given number of elevators
        elevator_system.__init__(num_elevators)
        return JsonResponse({'success': 'Elevator system initialized'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
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

@csrf_exempt
def save_user_request(request):
    """Save a user request to the list of requests for an elevator."""
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request method'}, status=405)

        floor = int(request.POST.get('floor'))

        if not floor:
            return JsonResponse({'error': 'Floor must be provided'},status=400)
     # Call the elevator system to handle the request
        elevator_system.call_elevator(floor)
        return JsonResponse({'success': 'Request added to elevator queue'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
@csrf_exempt
def request_to_move_current_elevator(request):
    """Requests for current elevator to move to destination."""
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request method'}, status=405)

        floor = int(request.POST.get('floor'))
        elevator_id = int(request.POST.get('elevator_id'))
        if not floor:
            return JsonResponse({'error': 'Floor must be provided'},status=400)
     # Call the elevator system to handle the request
        elevator_system.go_to_destination(elevator_id, floor)
        return JsonResponse({'success': 'Request added to elevator queue'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def mark_elevator_as_not_working(request, elevator_id):
    """Mark an elevator as not working or in maintenance."""
    try:
        elevator = Elevator.objects.get(pk=elevator_id)
        elevator.is_working = False
        elevator.save()

        return JsonResponse({'success': 'Elevator marked as not working'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def set_door_status(request, elevator_id):
    """Set the door status of an elevator."""
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Invalid request method'}, status=405)

        status = request.POST.get('is_open')
        if not status:
            return JsonResponse({'error': 'Door status must be provided'}, status=400)
        elevator = Elevator.objects.get(pk=elevator_id)
        elevator.doors_open = True if status.lower() == 'true' else False
        elevator.save()

        return JsonResponse({'success': 'Door status set'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_elevator_status(request, elevator_id):
    """Get the current status of an elevator."""
    try:
        elevator = Elevator.objects.get(pk=elevator_id)
        status = {
            'current_floor': elevator.floor,
            'movement': elevator.movement,
            'is_door_open': elevator.doors_open,
            'is_working': elevator.operational,
        }
        return JsonResponse({'status': status}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_elevator_list(request):
    """Get a list of all elevators in the system."""
    try:
        elevators = Elevator.objects.all()

        elevator_list = []
        for elevator in elevators:
            data = {
                'id': elevator.id,
                'current_floor': elevator.floor,
                'movement': elevator.movement,
                'is_door_open': elevator.doors_open,
                'is_working': elevator.operational,
                'num_requests': elevator.requests.count(),
            }
            elevator_list.append(data)

        return JsonResponse({'elevators': elevator_list}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_request_list(request):
    """Get a list of all requests in the system."""
    try:
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
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def emergency_stop(request, elevator_id):
    """Immediately stop an elevator in case of an emergency."""
    try:
        elevator = Elevator.objects.get(pk=elevator_id)
        elevator.movement = 'stopped'
        elevator.doors_open = True
        elevator.save()

        return JsonResponse({'success': 'Elevator stopped'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

