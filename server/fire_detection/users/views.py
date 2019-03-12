from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.db.models import Count, Q
import requests
from django.utils.timezone import now
from management.models import Users, Devices, Fires
import random

import json
import os
import string

from django.db import connection
from django.conf import settings
from django.utils import timezone

# Create your views here.

def login(request):
	if request.method == 'POST':
		# Try to log user
		_username = request.POST.get('username', '')
		_password = request.POST.get('password', '')

		x = Users.objects.filter(username = _username, password = _password)
		print(type(x))
		if not x:
			response_data = {}
			response_data['pk'] = -1
			return HttpResponse(json.dumps(response_data), content_type="application/json")

		else:
			_devices = Devices.objects.filter( user = x[0])
			print('siim')
			response = serialize("json", _devices)	
			return HttpResponse(response, content_type = 'application/json')
	return HttpResponse('<p> oii? </p>')


def signUp(request):
	if request.method == 'POST':
		_username = request.POST.get('username', '')
		auxUser = Users.objects.filter(username = _username)
		
		if not auxUser:
			_password = request.POST.get('password', '')
			_user = Users(username = str(_username), password = str(_password))
			_user.save()
			_dev = Devices(_id = 2, user = _user, token = '2jkjk')
			_dev.save()
		return HttpResponse('<p> ollll </p>')

def addDevice(request):
	if request.method == 'POST':
		_deviceToken = request.POST.get('deviceToken','')
		_username = request.POST.get('username','')
		auxDevice = Devices.objects.filter(token = _deviceToken )
		if auxDevice.count()>0:
			Devices.objects.filter(token = _deviceToken).update(user = _username)




def fires(request):
	x = Devices.objects.all()
	print(x)
	return HttpResponse('<p>Return fires </p>')

def actualState(request):
	return HttpResponse('<p>actualState</p>')

def temperature(request):
	return HttpResponse('<p> temperature</p>')

def humidity(request):
	return HttpResponse('<p> humidity </p>')

def carbon(request):
	return HttpResponse('<p> carbon </p>')