from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.db.models import Count, Q
import requests
from django.utils.timezone import now
from management.models import Users, Devices, Fires, Secrets, Conditions
import random

import json
import os
import string

from django.db import connection
from django.conf import settings
from django.utils import timezone

# Create your views here.


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

		x = Users.objects.filter(username = _username, password = _password)
		if x.count() == 0:
			response_data = {}
			response_data['check'] = 0

		else:	
			response_data = {}
			response_data['check'] = 1

		return HttpResponse(json.dumps(response_data), content_type="application/json")

	else:
		return HttpResponse('<p> oii? </p>')



def Devicesx(request):
	# if is POST REPOST is to insert new device
	if request.method == 'POST':
		_deviceToken = request.POST.get('token','')
		_localization = request.POST.get('localization','')
		_username = request.POST.get('username','')
		auxDevice = Devices.objects.all()

		if auxDevice.count()>0:
			Devices.objects.filter(token = _deviceToken).update(username = _username,localization = _localization)
			response_data = {}
			response_data['check'] = 1
		else:
			response_data = {}
			response_data['check'] = 0

		return HttpResponse(json.dumps(response_data), content_type="application/json")


	# if it is GET REQUEST we have to list all devices
	else:
		_username = request.POST.get('username','')
		_password = request.POST.get('password','')
		_user = Users.objects.filter(username = _username, password = _password)
		if _user.exists():
			_devices = Devices.objects.filter( user = _user[0].username)
			response = serialize("json", _devices)
			return HttpResponse(response, content_type = 'application/json')
		else:
			return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)
	


def fires(request):
	_username = request.POST.get('username','')
	_password = request.POST.get('password','')
	_user = Users. objects.filter(username = _username, password = _password)

	if _user.count() > 0:
		_deviceId = request.POST.get('id','')
		_device = Devices.objects.filter(_id = _deviceId )
		allFires = Devices.objects.filter( device = _device )
		response = serialize("json", allFires)
		return HttpResponse(response, content_type = 'application/json')
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)



def actualState(request):
	_username = request.POST.get('username','')
	_password = request.POST.get('password','')
	_user = Users. objects.filter(username = _username, password = _password)

	if _user.count() > 0:
		_deviceId = request.POST.get('id','')
		_device = Devices.objects.filter( _id = _deviceId )
		_conditions = Conditions.objects.filter( user = _device[0]).order_by('date').first()
		print(_conditions)
		return HttpResponse('<p>actualState</p>')
	else:
		return HttpResponse("Error: Invalid Request", content_type = "text/plain", status = 400)


def temperature(request):
	return HttpResponse('<p> temperature</p>')

def humidity(request):
	return HttpResponse('<p> humidity </p>')

def carbon(request):
	return HttpResponse('<p> carbon </p>')