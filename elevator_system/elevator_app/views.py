from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import Elevator, FloorRequest
from .controller import ElevatorSystemController
from .serializers import ElevatorSerializer, ElevatorSystemSerializer, FloorRequestSerializer, MarkElevatorSerializer, UserRequestSerializer, ElevatorDestinationSerializer

# Initialize the elevator system with 5 elevators
elevator_system = ElevatorSystemController(5)


class ElevatorActionViewSet(ViewSet):

    @action(detail=False, methods=['post'])
    def initialize_elevator_system(self, request):
        """Initialize the elevator system with a given number of elevators."""
        try:
            serializer = ElevatorSystemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            num_elevators = serializer.validated_data.get('num_elevators')

            # Initialize the elevator system with the given number of elevators
            elevator_system.__init__(num_elevators)
            return Response({'success': 'Elevator system initialized'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=True)
    def get_next_destination_for_elevator(self, request, pk):
        """Get the next destination floor for a given elevator."""
        try:
            elevator = Elevator.objects.get(pk=pk)
            if not elevator.requests.exists():
                return Response({'error': 'No requests for this elevator'}, status=status.HTTP_404_NOT_FOUND)

            next_request = elevator.requests.first()
            serializer = FloorRequestSerializer(next_request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def request_to_move_current_elevator(self, request):
        """Requests for current elevator to move to destination."""
        try:
            serializer = ElevatorDestinationSerializer(data=request.data)
            if serializer.is_valid():
                elevator_id = serializer.validated_data.get('elevator_id')
                floor = serializer.validated_data.get('floor')
                # Call the elevator system to handle the request
                elevator_system.go_to_destination(elevator_id, floor)
                return Response({'success': 'Request added to elevator queue'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=True)
    def emergency_stop(self, request, pk):
        """Immediately stop an elevator in case of an emergency."""
        try:
            elevator = Elevator.objects.get(pk=pk)
            elevator.movement = 'stopped'
            elevator.doors_open = True
            elevator.save()
            return Response({'success': 'Elevator stopped'}, status=status.HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ElevatorMovementViewSet(ViewSet):
    def retrieve(self, request, pk):
        """Get if the elevator is moving up or down currently."""
        try:
            elevator = Elevator.objects.get(pk=pk)
            return Response({'movement': elevator.movement}, status=status.HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRequestViewSet(ViewSet):
    """Save a user request to the list of requests for an elevator."""

    def create(self, request):
        serializer = UserRequestSerializer(data=request.data)
        if serializer.is_valid():
            floor = serializer.validated_data.get('floor')
            elevator_system.call_elevator(floor)
            return Response({'success': 'Request added to elevator queue'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetElevatorStatusView(ViewSet):
    @action(detail=False, methods=['post'])
    def mark_elevator_as_not_working(self, request):
        """Mark an elevator as not working or in maintenance."""
        try:

            serializer = MarkElevatorSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            elevator_id = serializer.validated_data.get('elevator_id')
            state = serializer.validated_data.get('state')
            elevator = Elevator.objects.get(pk=elevator_id)
            elevator.operational = state
            elevator.save()
            if state:
                return Response({'success': 'Elevator marked as working'}, status=status.HTTP_200_OK)
            else:
                return Response({'success': 'Elevator marked as not working'}, status=status.HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def set_door_status(self, request):
        """Set the door status of an elevator."""
        try:
            serializer = MarkElevatorSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            elevator_id = serializer.validated_data.get('elevator_id')
            state = serializer.validated_data.get('state')
            elevator = Elevator.objects.get(pk=elevator_id)
            elevator.doors_open = state
            elevator.save()
            return Response({'success': 'Door status set'}, status=status.HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ElevatorViewSet(ViewSet):

    def retrieve(self, request, pk):
        """Get the current status of an elevator."""
        try:
            elevator = Elevator.objects.get(pk=pk)
            serializer = ElevatorSerializer(elevator)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Get a list of all elevators in the system."""
        try:
            elevators = Elevator.objects.all()
            serializer = ElevatorSerializer(elevators, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FloorRequestViewSet(ViewSet):

    def retrieve(self, request, pk):
        """Get all requests for a given elevator."""
        try:
            elevator = Elevator.objects.get(pk=pk)
            requests = elevator.requests.all()
            serializer = FloorRequestSerializer(requests, many=True)
            return Response({'requests': serializer.data}, status=status.HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Get a list of all requests in the system."""
        try:
            requests = FloorRequest.objects.all()
            serializer = FloorRequestSerializer(requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
