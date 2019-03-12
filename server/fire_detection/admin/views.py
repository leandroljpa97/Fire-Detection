from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.db.models import Count, Q
import requests
from django.utils.timezone import now
from management.models import Users, Devices, Fires


import json
import os
import string

from django.db import connection
from django.conf import settings
from django.utils import timezone

# Create your views here.

def login(request):
	return HttpResponse('<p>login Admin</p>')

def users(request):
	return HttpResponse('<p> users </p>')

def addUser(request):
	return HttpResponse('<p> Add new user </p>')

def thresholds(request):
	return HttpResponse('<p> thresholds </p>')

def devices(request):
	return HttpResponse('<p>devices</p>')
	

def addDevice(request):
	if request.method == POST:

		while True:
			_token = random.randint(1, 101)
			aux = Devices.objectss.filter(token = _token )
			if not aux:
				break
	return HttpResponse('<p> Add new device </p>')


def fires(request):
	return HttpResponse('<p> firessAdmin </p>')

def temperature(request):
	return HttpResponse('<p> temperature</p>')

def humidity(request):
	return HttpResponse('<p> humidity </p>')

def carbon(request):
	return HttpResponse('<p> carbon </p>')