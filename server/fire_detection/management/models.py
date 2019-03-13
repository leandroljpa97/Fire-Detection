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
	token = models.CharField(max_length = 255)
	localization = models.CharField(max_length = 255)

	def __str__(self):
		return self.token

class Fires(models.Model):
	date =  models.DateTimeField(default = timezone.now)
	device = models.ForeignKey(Devices, on_delete=models.CASCADE, related_name='devicesFire')
	description = models.CharField(max_length = 255)
	def __str__(self):
		return self.device

class Conditions(models.Model):
	device = models.ForeignKey(Devices, on_delete=models.CASCADE, related_name='devicesCondit')
	temperature = models.IntegerField() 
	humidity = models.IntegerField() 
	carbon = models.IntegerField() 
	date = models.DateTimeField(default = timezone.now)
	def __str__(self):
		return self.date

class Secrets(models.Model):
	secret = models.IntegerField() 
	def __str__(self):
		return self.secret


