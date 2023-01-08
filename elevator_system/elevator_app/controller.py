from .models import Elevator, FloorRequest, Floor

class ElevatorSystemController:
    def __init__(self, num_elevators, num_floors=10):
        self.num_elevators = num_elevators
        self.elevators = []
        self.floors = []

        # Create the elevators and floors
        for i in range(num_elevators):
            elevator = Elevator.objects.create()
            self.elevators.append(elevator)

        for i in range(num_floors):
            floor = Floor.objects.create(number=i+1)
            self.floors.append(floor)

    def call_elevator(self, floor_number, direction):
        """Called when a user pushes the button on a floor to request an elevator."""
        # Create a request for the elevator
        request = FloorRequest.objects.create(floor=floor_number, direction=direction)

        # Find the most optimal elevator for the request
        optimal_elevator = self.find_optimal_elevator(request)
        optimal_elevator.assign_request(request)

        # Move the elevator to the requested floor
        optimal_elevator.decide_movement()

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
    
    
