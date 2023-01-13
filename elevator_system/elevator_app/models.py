from django.db import models

class Elevator(models.Model):
    # Fields for the elevator's current status
    UP = 'UP'
    DOWN = 'DOWN'
    STOPPED = 'STOPPED'
    MOVEMENT_CHOICES = [
        (UP, 'Up'),
        (DOWN, 'Down'),
        (STOPPED, 'Stopped'),
    ]
    movement = models.CharField(
        max_length=8,
        choices=MOVEMENT_CHOICES,
        default=STOPPED,
    )
    floor = models.PositiveIntegerField(default=1)
    doors_open = models.BooleanField(default=False)

    # Fields for handling requests
    requests = models.ManyToManyField('FloorRequest', blank=True)

    # Additional fields for the elevator system
    available = models.BooleanField(default=True)
    operational = models.BooleanField(default=True)

    def move_up(self):
        self.movement = self.UP
        self.save()

    def move_down(self):
        self.movement = self.DOWN
        self.save()

    def stop(self):
        self.movement = self.STOPPED
        self.save()

    def open_doors(self):
        self.doors_open = True
        self.save()

    def close_doors(self):
        self.doors_open = False
        self.save()

    def decide_movement(self, current_request):
        if not self.requests.exists():
            self.stop()
            return
        if current_request.floor > self.floor:
            self.move_up()
        elif current_request.floor < self.floor:
            self.move_down()
        else:
            self.stop()

    def assign_request(self, request):
        """Assign a request to this elevator and mark it as not available."""
        self.requests.add(request)
        self.available = False
        self.save()

    def complete_request(self, request):
        """Remove a request from this elevator and mark it as available."""
        self.floor = request.floor
        self.available = True
        self.movement = self.STOPPED
        self.save()

    def __str__(self):
        return f'Elevator {self.id} on floor {self.floor} with are doors open {self.doors_open}'
    

class FloorRequest(models.Model):
    floor = models.PositiveIntegerField()
    
    def __str__(self):
        return f'Request to go floor {self.floor}'
    
