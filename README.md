# Elevator-system

Steps to stepup and deploy
Create database in your postgres with any name 
Add you database creds in the .env 
You need to install python 3.10
Create new virtual env using cmd “virtualenv -p python3.10 venv”
Activate virtual environment “source venv/bin/activate”
Install requirement from requirement.txt “pip install -r requirement.txt”
Create migrations file on database using “./manage.py makemigrations  elevator_app”
Run migrations  “./manage.py migrate  elevator_app”
After that you can start the project using “./manage.py runserver”
	
Database modeling:-
For database models(Entity) I used two models 
The first Elevator is the primary model which handles all the elevator’s state and 
The Second is FloorRequest which handles the request

	Elevator have the following according to my understanding of the problem

Movement : which stores the movement to current Elevator  
floor : which at which floor elevator is on
Doors_open : state of door is closed or open
requests : stores the request associated with elevator
available : is avialabe to sever other requests
Operational : is working or not

FloorRequest is pretty simple just holds the requests

Service layer(ElevatorSystemController):-
It handling most of the main logic like initilization, finding optimal elevator and call elevator 


API Endpoints:-
https://www.postman.com/shubhamparashar210/workspace/work/collection/12549211-9f2c87c7-e1a7-49e8-971d-578a26676926?action=share&creator=12549211

