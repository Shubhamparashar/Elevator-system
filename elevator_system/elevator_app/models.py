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
    floor = models.PositiveIntegerField()
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

    def decide_movement(self):
        if not self.requests.exists():
            self.stop()
            return

        current_request = self.requests.first()
        if current_request.direction == self.UP:
            self.move_up()
        elif current_request.direction == self.DOWN:
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
        self.requests.remove(request)
        self.available = True
        self.save()

    def __str__(self):
        return f'Elevator {self.pk} on floor {self.floor} going {self.movement} with doors {self.doors_open}'
    

class FloorRequest(models.Model):
    UP = 'UP'
    DOWN = 'DOWN'
    DIRECTION_CHOICES = [
        (UP, 'Up'),
        (DOWN, 'Down'),
    ]
    direction = models.CharField(
        max_length=4,
        choices=DIRECTION_CHOICES,
    )
    floor = models.PositiveIntegerField()

    def __str__(self):
        return f'Request to go {self.direction} from floor {self.floor}'