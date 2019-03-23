from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name='admin'

urlpatterns = [
	path('', csrf_exempt(views.login), name = 'loginAdmin'),
	path('users/', csrf_exempt(views.users), name = 'allUsers'),
	path('devices/', csrf_exempt(views.devices), name = 'allDevices'),
	path('device/', csrf_exempt(views.addDevice), name = 'addDevice'),
	path('thresholds/', csrf_exempt(views.thresholds), name = 'thresholds'),
	path('fires/', csrf_exempt(views.fires), name = 'fires'),
	path('allFires/', csrf_exempt(views.allFires), name = 'Afires'),
	path('periodic/', csrf_exempt(views.downlink), name = 'periodic'),
    ]
