from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.db.models import Count, Q
import requests
from django.utils.timezone import now
from management.models import Users, Devices, Fires, Secrets, Conditions
import random
import ast


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
carbonTh = 0


def checkAdmin(request):
	_secret = request.POST.get('secret', '')
	aux = Secrets.objects.filter(secret = _secret)
	if aux.count() > 0:
		return 1
	return 0

def login(request):
	if request.method == 'POST':
		# Try to log admin
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		if username == 'admin' and password == '123':
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
	global carbonTh

	if request.method == 'POST':
		if not checkAdmin(request):
			return HttpResponse("Error: Invalid Login", content_type = "text/plain", status = 401)
		print('ola')
		humidityTh = int(ast.literal_eval(request.POST.get('humidity', '')))
		temperatureTh = int(ast.literal_eval(request.POST.get('temperature', '')))
		carbonTh = int(ast.literal_eval(request.POST.get('carbon', '')))
		print(carbonTh)
		print(type(carbonTh))
		responseData = {}
		responseData['check'] = 1
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
				auxDev = Devices.objects.all()
				lastDevice= Devices.objects.order_by('_id').last()
				if auxDev.count() == 0:
					newId = 1
				else:
					newId = lastDevice._id + 1
				print(newId)
				newDevice = Devices(_id = newId , username = 'NULL' , token = _token, localization = 'NULL' )
				newDevice.save()
				responseData = {}
				responseData['token'] = _token
				return HttpResponse(json.dumps(responseData), content_type="application/json")


		




def fires(request):
	return HttpResponse('<p> firessAdmin </p>')

def temperature(request):
	return HttpResponse('<p> temperature</p>')

def humidity(request):
	return HttpResponse('<p> humidity </p>')

def carbon(request):
	return HttpResponse('<p> carbon </p>')