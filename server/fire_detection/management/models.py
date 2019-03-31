from django.db import models
from django.utils import timezone

# Create your models here.

class Users(models.Model):
	username = models.CharField(max_length = 255, primary_key = True)
	password = models.CharField(max_length = 255)

	def __str__(self):
		return self.username

class Devices(models.Model):
	_id = models.IntegerField(primary_key = True) 
	username = models.CharField(max_length = 255)
	token = models.IntegerField()
	localization = models.CharField(max_length = 255)

	def __str__(self):
		return self.token

class Fires(models.Model):
	_id = models.IntegerField(primary_key = True) 
	date =  models.DateTimeField(default = timezone.now)
	device = models.IntegerField()
	description = models.CharField(max_length = 255)
	def __str__(self):
		return self.device

class Conditions(models.Model):
	device = models.IntegerField()
	temperature = models.IntegerField() 
	humidity = models.IntegerField() 
	gas = models.IntegerField()
	date = models.DateTimeField(default = timezone.now)
	def __str__(self):
		return self.date

class Secrets(models.Model):
	secret = models.IntegerField() 
	def __str__(self):
		return self.secret

class Notifications(models.Model):
	email = models.CharField(max_length = 255)
	def __str__(self):
		return self.email



