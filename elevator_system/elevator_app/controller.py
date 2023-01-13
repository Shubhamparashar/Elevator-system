from .models import Elevator, FloorRequest

class ElevatorSystemController:
    def __init__(self, num_elevators):
        self.num_elevators = num_elevators
        self.elevators = []
        self.floors = []

        # Create the elevators and floors
        last_elevator = Elevator.objects.last()
        last_elevator_number = last_elevator.id if last_elevator else 0

        if last_elevator_number > num_elevators:
            elevators = Elevator.objects.filter(id__lte=num_elevators)
            self.elevators.extend(elevators)
        else:
            elevators = Elevator.objects.filter(id__lte=last_elevator_number)
            self.elevators.extend(elevators)    
            for i in range(last_elevator_number, num_elevators):
                elevator = Elevator.objects.create()
                self.elevators.append(elevator)


    def call_elevator(self, floor_number):
        """Called when a user pushes the button on a floor to request an elevator."""
        # Create a request for the elevator
        request = FloorRequest.objects.create(floor=floor_number)

        # Find the most optimal elevator for the request
        optimal_elevator = self.find_optimal_elevator(request)
        optimal_elevator.assign_request(request)

        # Move the elevator to the requested floor
        optimal_elevator.decide_movement()
        
        optimal_elevator.complete_request(request)

    def find_optimal_elevator(self, request):
        """Find the most optimal elevator for a given request."""
        optimal_elevator = None
        min_distance = float('inf')

        for elevator in self.elevators:
            if not elevator.operational:
                continue
            distance = abs(elevator.floor - request.floor)
            if distance < min_distance:
                optimal_elevator = elevator
                min_distance = distance
        
        return optimal_elevator
    
    def go_to_destination(self, elevator_id, floor_number):
        """Called when a user pushes the button on a floor to request an elevator."""
        elevator = Elevator.objects.get(pk=elevator_id)
        # Create a request for the elevator
        request = FloorRequest.objects.create(floor=floor_number)

        # Assign request to the elevator
        elevator.assign_request(request)

        # Decide movement of the elevator 
        elevator.decide_movement()
        
        # Move the elevator to the requested floor
        elevator.complete_request(request)
    
