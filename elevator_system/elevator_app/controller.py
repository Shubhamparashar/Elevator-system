from .models import Elevator, FloorRequest, Floor

class ElevatorSystemController:
    def __init__(self, num_elevators, num_floors=10):
        self.num_elevators = num_elevators
        self.elevators = []
        self.floors = []

        # Create the elevators and floors
        last_elevator = Elevator.objects.last()
        last_elevator_number = last_elevator.elevator_number if last_elevator else 0

        if last_elevator_number > num_elevators:
            elevators = Elevator.objects.filter(elevator_number__lte=num_elevators)
            self.elevators.extend(elevators)
        else:
            elevators = Elevator.objects.filter(elevator_number__lte=last_elevator_number)
            self.elevators.extend(elevators)    
            for i in range(last_elevator_number, num_elevators):
                elevator = Elevator.objects.create(elevator_number=i)
                self.elevators.append(elevator)


        last_floor = Floor.objects.last()
        last_floor_number = last_floor.number if last_floor else 0

        if last_floor_number > num_floors:
            floors = Floor.objects.filter(number__lte=num_floors)
            self.floors.extend(floors)
        else:
            floors = Floor.objects.filter(number__lte=last_floor_number)
            self.floors.extend(floors)    
            for i in range(last_floor_number, num_floors):
                floor = Floor.objects.create(number=i)
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
    
    
