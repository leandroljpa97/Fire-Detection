from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.db.models import Count, Q
import requests
from django.utils.timezone import now
from management.models import Users, Devices, Fires, Secrets, Conditions
import random
import ast
from users.views import bombState, alarmState, alarmEnable
import json
import os
import string

from django.db import connection
from django.conf import settings
from django.utils import timezone

# Create your views here.

#threshold default values
temperatureTh = 0
humidityTh = 0
gasTh = 0



def checkAdmin(request):
	_secret = int(ast.literal_eval(request.POST.get('secret', '')))
	aux = Secrets.objects.filter(secret = _secret)
	if aux.count() > 0:
		return 1
	return 0



def login(request):
	if request.method == 'POST':
		# Try to log admin
		username = request.POST.get('username', '')
		password =  int(ast.literal_eval(request.POST.get('password', '')))
		if username == 'admin' and password == 123:
			while True:
				_secret = random.randint(1, 1000)
				aux = Secrets.objects.filter(secret = _secret)
				print(aux.count())
				if aux.count() == 0:
					newSecret = Secrets(secret = _secret)
					newSecret.save()
					responseData = {}
					responseData['secret'] = _secret
					break;
		else:
			responseData = {}
			responseData['secret'] = -1
		return HttpResponse(json.dumps(responseData), content_type="application/json")


		

def users(request):
	if request.method == 'POST':
		if not checkAdmin(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_users = Users.objects.all()
		response = serialize("json", _users)
		return HttpResponse(response, content_type = 'application/json')

def thresholds(request):
	global humidityTh
	global temperatureTh
	global gasTh

	if request.method == 'POST':
		if not checkAdmin(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)
		humidityTh = int(ast.literal_eval(request.POST.get('humidity', '')))
		temperatureTh = int(ast.literal_eval(request.POST.get('temperature', '')))
		gasTh = int(ast.literal_eval(request.POST.get('gas', '')))


		responseData = {}
		responseData['check'] = 1
		return HttpResponse(json.dumps(responseData), content_type="application/json")
	else:
		responseData = {}
		responseData['humidity'] = humidityTh
		responseData['temperature'] = temperatureTh
		responseData['gas'] = gasTh
		return HttpResponse(json.dumps(responseData), content_type="application/json")



def devices(request):
	if request.method == 'POST':
		if not checkAdmin(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_devices = Devices.objects.all()
		response = serialize("json", _devices)
		return HttpResponse(response, content_type = 'application/json')
	

def addDevice(request):
	if request.method == 'POST':
		if not checkAdmin(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		while True:
			_token = random.randint(1, 1000)
			aux = Devices.objects.filter(token = _token )
			if aux.count() == 0:
				devId = int(ast.literal_eval(request.POST.get('id','')))
				print(devId)
				_aux = Devices.objects.filter(_id = devId)
				if _aux.count() == 0:
					newDevice = Devices(_id = devId , username = 'NULL' , token = _token, localization = 'NULL' )
					newDevice.save()
					responseData = {}
					responseData['token'] = _token
					return HttpResponse(json.dumps(responseData), content_type="application/json")
				else:
					responseData = {}
					responseData['token'] = -1
					return HttpResponse(json.dumps(responseData), content_type="application/json")





def allFires(request):
	if request.method == 'POST':
		if not checkAdmin(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)

		_fires = Fires.objects.all()
		response = serialize("json", _fires)
		return HttpResponse(response, content_type = 'application/json')




def fires(request):
	if request.method == 'POST':
		if not checkAdmin(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)
		_id = int(ast.literal_eval(request.POST.get('id','')))
		_description = request.POST.get('description','')
		Fires.objects.filter(_id = _id).update(description = _description)
	return HttpResponse('<p> firessAdmin </p>')


def downlink(request):
	global temperatureTh 
	global humidityTh
	global gasTh
	global alarmEnable
	global alarmState
	global bombState

	if len(str(temperatureTh)) == 1 :
		print(temperatureTh)
		auxTemp = "0"+ str(temperatureTh)
	else:
		auxTemp = str(temperatureTh)

	if len(str(humidityTh)) == 1 :
		auxHum = "0"+ str(humidityTh)
	else:
		auxHum = str(humidityTh)

	if len(str(gasTh)) == 1 :
		auxGas = "0"  + str(gasTh)
	else:
		auxGas = str(gasTh)


	sendData = auxTemp + auxHum + auxGas + str(alarmEnable) + str(alarmState) + str(bombState) + "0000000"
	
	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)
		_data = body['data']
		
		if int(ast.literal_eval(_data)) == 1:
			return HttpResponse(status = 204)
		
		deviceId = int(ast.literal_eval(body['device']))
		return HttpResponse(json.dumps({deviceId: {"downlinkData": sendData}}), content_type="application/json")
	
	return HttpResponse(status = 204)
		


def deleteUser(request):
	if request.method == 'POST':
		_name = request.POST.get('username', '')
		Users.objects.filter(username= _name).delete()
		return HttpResponse(status = 204)

def deleteDevice(request):
	if request.method == 'POST':
		id = request.POST.get('id', '')
		Devices.objects.filter(_id = id).delete()
		return HttpResponse(status = 204)
