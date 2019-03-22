from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.db.models import Count, Q
import requests
from django.utils.timezone import now
from management.models import Users, Devices, Fires, Secrets, Conditions
# from pusher_push_notifications import PushNotifications
import random
import ast


import json
import os
import string

from django.db import connection
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import now


# Create your views here.

def checkUser(request):
	_username = request.POST.get('username','')
	_password = request.POST.get('password','')

	usersAux = Users.objects.filter(username = _username).filter(password = _password)
	if usersAux.count() > 0:
		return 1

	return 0

def signUp(request):
	if request.method == 'POST':
		_username = request.POST.get('username', '')
		auxUser = Users.objects.filter(username = _username)

		#check if user not exists yet
		if auxUser.count() == 0:
			_password = request.POST.get('password', '')
			_user = Users(username = _username, password = _password)
			_user.save()
			response_data = {}
			response_data['check'] = 1
		else:
			response_data = {}
			response_data['check'] = 0

		return HttpResponse(json.dumps(response_data), content_type="application/json")

def login(request):
	if request.method == 'POST':
		# Try to log user
		_username = request.POST.get('username', '')
		_password = request.POST.get('password', '')

		x = Users.objects.filter(username = _username).filter(password = _password)
		if x.count() == 0:
			response_data = {}
			response_data['check'] = 0

		else:
			response_data = {}
			response_data['check'] = 1

		return HttpResponse(json.dumps(response_data), content_type="application/json")

	else:
		response = render(request, './index.html')
		return response



def DevicesUpd(request):
	# if is POST REPOST is to insert new device
	if request.method == 'POST':
		if not checkUser(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_deviceToken = request.POST.get('token','')
		_localization = request.POST.get('localization','')
		_username = request.POST.get('username','')
		auxDevice = Devices.objects.all()

		if auxDevice.count()>0:
			Devices.objects.filter(token = _deviceToken).update(username = _username, localization = _localization)
			response_data = {}
			response_data['check'] = 1
		else:
			response_data = {}
			response_data['check'] = 0

		return HttpResponse(json.dumps(response_data), content_type="application/json")

def ListAllDevices(request):
	# if it is GET REQUEST we have to list all devices
	if request.method == 'POST':
		if not checkUser(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_username = request.POST.get('username','')

		_devices = Devices.objects.filter( username = _username)
		response = serialize("json", _devices)
		return HttpResponse(response, content_type = 'application/json')



def fires(request):
	if request.method == 'POST':
		if not checkUser(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_token = request.POST.get('token','')
		_device = Devices.objects.filter(token = _token)
		allFires = Devices.objects.filter( device = _device )
		response = serialize("json", allFires)
		return HttpResponse(response, content_type = 'application/json')




def actualState(request):
	if request.method == 'POST':
		if not checkUser(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_token = request.POST.get('token','')
		_device = Devices.objects.filter( token = _token )
		_conditions = Conditions.objects.filter( device= _device[0]).order_by('date').last()
		response_data = {}
		response_data['humidity'] = _conditions.humidity
		response_data['temperature'] = _conditions.temperature
		response_data['carbon'] = _conditions.carbon
		return HttpResponse(json.dumps(response_data), content_type="application/json")



def temperature(request):
	if request.method == 'POST':
		_token = request.POST.get('token','')
		auxDevice = Devices.objects.filter(token= _token)
		_conditions = Conditions.objects.filter(device = auxDevice[0])
		response = serialize("json", _conditions)
		return HttpResponse(response, content_type = 'application/json')

	return HttpResponse('<p> temperature</p>')

def humidity(request):
	return HttpResponse('<p> humidity </p>')

def carbon(request):
	return HttpResponse('<p> carbon </p>')

def getValuesArduino(request):
	if request.method == 'POST':
		print('entrei')
		_humidity = int(ast.literal_eval(request.POST.get('humidity','')))
		_temperature = int(ast.literal_eval(request.POST.get('temperature','')))
		_carbon = int(ast.literal_eval(request.POST.get('carbon','')))
		_id = request.POST.get('id','')

		auxDevice = Devices.objects.filter(_id = _id)
		newConditions = Conditions(device = auxDevice[0], temperature= _temperature, humidity = _humidity, carbon = _carbon, date = now())
		newConditions.save()
		response_data = {}
		response_data['check'] = 1

		return HttpResponse(json.dumps(response_data), content_type="application/json")

"""
def Fresh(request):
	Users.objects.all().delete()
	Devices.objects.all().delete()
	Fires.objects.all().delete()
	Conditions.objects.all().delete()
	Secrets.objects.all().delete()

def Push(request):
	beams_client = PushNotifications(
		instance_id = '1a81f3fb-fa47-4820-9742-bf752a077700',
		secret_key = '5BCD4BB732BD48B78403BD3A35B2946A1B9FF58DD90D5B3F8AB938AE68EBE235',
	)

	response = beams_client.publish_to_interests(
	    interests=[ 'Leandroo'],
	    publish_body={
		'apns': {
		    'aps': {
		        'alert': 'Hello!'
		    }
		},
		'fcm': {
		    'notification': {
		        'title': 'Hello',
		        'body': 'Hello, World!'
		    }
		}
	    }
	)

	responsee = beams_client.publish_to_interests(
	    interests=[ 'Leandro'],
	    publish_body={
		'apns': {
		    'aps': {
		        'alert': 'Benfica!'
		    }
		},
		'fcm': {
		    'notification': {
		        'title': 'Benfica',
		        'body': 'Hello, World!!!'
		    }
		}
	    }
	)


	print(response['publishId'])
	return HttpResponse('<p> Push <p>')

"""
