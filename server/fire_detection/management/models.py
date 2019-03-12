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
	user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user')
	token = models.CharField(max_length = 255)

	def __str__(self):
		return self.token

class Fires(models.Model):
	date =  models.DateTimeField(default = timezone.now)
	device = models.ForeignKey(Devices, on_delete=models.CASCADE, related_name='devices')
	description = models.CharField(max_length = 255)
	def __str__(self):
		return self.device

class Conditions(models.Model):
	temperature = models.IntegerField() 
	humidity = models.IntegerField() 
	carbon = models.IntegerField() 
	date = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.date