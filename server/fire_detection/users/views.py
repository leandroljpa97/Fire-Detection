from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.db.models import Count, Q
import requests
from django.utils.timezone import now
from management.models import Users, Devices, Fires, Secrets, Conditions, Notifications
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
from django.forms.models import model_to_dict


alarmState = 0
bombState = 0
alarmEnable = 0


# Create your views here.



def checkUser(request):
	_username = request.POST.get('username','')
	_password = request.POST.get('password','')

	usersAux = Users.objects.filter(username = _username).filter(password = _password)
	if usersAux.count() > 0:
		return 1

	return 0

def aux(request):
	_fire = Fires(_id = 15, date = now(), device = 12, description = 'Solved Fire')
	_fire.save()
	_fire2 = Fires(_id = 72, date = now(), device = 10, description = 'dangerous fire in Kitchen')
	_fire2.save()
	_fire3 = Fires(_id = 310, date = now(), device = 10, description = 'COntrolled fire in Pedrogão Grande')
	_fire3.save()
	return HttpResponse("<p> olaa </p>")



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
		auxDevice = Devices.objects.filter(token = _deviceToken)

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

		_token = int(ast.literal_eval(request.POST.get('token','')))
		_device = Devices.objects.filter(token = _token)
		print(_device[0]._id)
		allFires = Fires.objects.filter( device = _device[0]._id )
		response = serialize("json", allFires)
		return HttpResponse(response, content_type = 'application/json')
	else:
		
		allFires=Fires.objects.all()
		fires= []
		for item in allFires:
			print(item.date)
			fires.insert(0,{'date':item.date, 'content':item.description })

		return JsonResponse({'fires':fires})




def actualState(request):
	global alarmEnable
	
	if request.method == 'POST':
		if not checkUser(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_token = int(ast.literal_eval(request.POST.get('token','')))
		_device = Devices.objects.filter( token = _token )
		_conditions = Conditions.objects.filter( device = _device[0]._id).order_by('date')
		response_data = {}
		if _conditions.count() > 0:
			_conditions = Conditions.objects.filter( device = _device[0]._id).order_by('date').last()
			response_data['humidity'] = _conditions.humidity
			print("conditions.humidity")
			print(_conditions.humidity)
			response_data['temperature'] = _conditions.temperature
			response_data['gas'] = _conditions.gas
			response_data['alarmEnable'] = alarmEnable
			print(response_data)
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		return HttpResponse(status = 204)



def saveMail(request):
	if request.method == 'POST':
		_email = str(request.POST.get('mail'))
		newmail = Notifications(email = _email)
		newmail.save()
		return HttpResponse(status=204)



def Fresh(request):
	Users.objects.all().delete()
	Devices.objects.all().delete()
	Fires.objects.all().delete()
	Conditions.objects.all().delete()
	Secrets.objects.all().delete()
	Notifications.objects.all().delete()


def Push(_device):
	beams_client = PushNotifications(
		instance_id = '1a81f3fb-fa47-4820-9742-bf752a077700',
		secret_key = '5BCD4BB732BD48B78403BD3A35B2946A1B9FF58DD90D5B3F8AB938AE68EBE235',
	)

	response = beams_client.publish_to_interests(
	    interests=[ str(_device)],
	    publish_body={
		'apns': {
		    'aps': {
		        'alert': 'Fire! Atention'
		    }
		},
		'fcm': {
		    'notification': {
		        'title': 'Atention, Fire in device '+ _device,
		        'body': 'Fire in device '+ _device
		    }
		}
	    }
	)


def newFire(_device):
	auxFire = Fires.objects.all()
	lastFire= Fires.objects.order_by('_id').last()
	if auxFire.count() == 0:
		newId = 1
	else:
		newId = lastFire._id + 1
		_newFire = Fires(_id = newId, date= now(), device = _device, description ='Admin did not put any description yet');
		_newFire.save()
		return HttpResponse('<p> New Fire </p>')


def getAlarmAndBombState(request):
	global alarmState 
	global bombState 


	response_data = {}
	response_data['alarm'] = alarmState
	response['bomb'] = bombState
	return HttpResponse(json.dumps(response_data), content_type="application/json")

def enableAlarm(request):
	global alarmEnable
	if request.method == "POST":
		alarmEnable = int(ast.literal_eval(request.POST.get('alarmEnable','')))
		return HttpResponse(status=204)
	return HttpResponse(status=204)


def Uplink(request):
	global alarmState
	global bombState

	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		#_data = request.POST.get('data','')
		_data = body['data']



		if int((_data)) ==1:
			print("isto e de downlink. nao e para mim, po crlh- sou")
			return HttpResponse(status=204)

		else:
			_id = int(body['device'])
			print(_id)
			# aux = str(int(ast.literal_eval(_data)))
			aux = _data
			out = [(aux[i:i+3]) for i in range(0, len(aux), 3)]
			
			_temperature = int((out[0]))
			print(_temperature)
			print(type(_temperature))
			x = 4
			print(type(x))
			_humidity =  int((out[1]))
			print(_humidity)
			_gas =  int((out[2]))
			print(_gas)
			## alarmState = int(ast.literal_eval(out[3]))
			## bombState = int(ast.literal_eval(out[4]))

			_fire =  int((out[3]))
			print(_fire)

			if _fire != 0:
				print(_fire)
				_device = Devices.objects.filter(_id = _id)
				_devId = _device[0]._id
				newFire(_devId)
				Push(_devId)

			newCondition = Conditions(device = _id, temperature = _temperature , humidity = _humidity,gas = _gas, date = now())
			newCondition.save()
		return HttpResponse(status=204)


