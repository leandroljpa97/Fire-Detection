# Fire-Detection


IOT fire detection system with 3 identities: Sensors (temperature, humidity and gas measurement) that are controlled through an arduino, REST API, developed in Django, associated with a Database that stores various information (is online at Google and we also have a website for the project), and android application which allows the user and the administrator to interact with the server and sensors. Communication from the sensors to the server is done through Rádio( SigFox ).

the arduino periodically sends in a specific format the values measured by the sensors, to the server, that stores in a database (with POST method). Then the android application makes GET and POST requests to interact with the server. 

In the application, the user can access the temperature, humidity, gas of their devices, that are set up where the user wants (kitchen, bedroom, ...). 
As soon as a fire occurs, all the users of a certain home receive notifications in the application, and the server send also information to the arduino to activate the water pump and the buzz alarm

All the explanations in RMSF___Interm_dio.pdf . 

final grade: 20/20
