from rest_framework import serializers
from .models import FloorRequest, Elevator


class ElevatorSerializer(serializers.ModelSerializer):
    num_requests = serializers.SerializerMethodField()

    class Meta:
        model = Elevator
        fields = ('id', 'floor', 'movement', 'doors_open', 'operational', 'num_requests')
        
    def get_num_requests(self, elevator):
        return elevator.requests.count()


class FloorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorRequest
        fields = ('id', 'floor')

class ElevatorSystemSerializer(serializers.Serializer):
    num_elevators = serializers.IntegerField()
    
        
class UserRequestSerializer(serializers.Serializer):
    floor = serializers.IntegerField()
    

class ElevatorDestinationSerializer(serializers.Serializer):
    elevator_id = serializers.IntegerField()
    floor = serializers.IntegerField()
    

class MarkElevatorSerializer(serializers.Serializer):
    state = serializers.BooleanField(default=False)
    elevator_id = serializers.IntegerField()
