from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.db.models import Count, Q
import requests
from django.utils.timezone import now

import json
import os
import string

from django.db import connection
from django.conf import settings
from django.utils import timezone

# Create your views here.

def login(request):
	return HttpResponse('<p>login User</p>')

def fires(request):
	return HttpResponse('<p>Return fires </p>')

def actualState(request):
	return HttpResponse('<p>actualState</p>')

def temperature(request):
	return HttpResponse('<p> temperature</p>')

def humidity(request):
	return HttpResponse('<p> humidity </p>')

def carbon(request):
	return HttpResponse('<p> carbon </p>')