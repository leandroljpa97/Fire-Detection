from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name='admin'

urlpatterns = [
	path('', csrf_exempt(views.login), name = 'loginAdmin'),
	path('users/', csrf_exempt(views.users), name = 'allUsers'),
	path('user/', csrf_exempt(views.addUser), name = 'addUser'),
	path('devices/', csrf_exempt(views.devices), name = 'allDevices'),
	path('device/', csrf_exempt(views.addDevice), name = 'addDevice'),
	path('thresholds/', csrf_exempt(views.thresholds), name = 'thresholds'),
	path('fires/', csrf_exempt(views.fires), name = 'fires'),
	path('temperature/', csrf_exempt(views.temperature), name = 'temperatureA'),
    path('humidity/', csrf_exempt(views.humidity), name = 'humidityA'),
    path('carbon/', csrf_exempt(views.carbon), name = 'carbonA'),



    ]
