from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name='users'

urlpatterns = [
	path('', csrf_exempt(views.login), name = 'loginUser'),
	path('signup/', csrf_exempt(views.signUp), name = 'signUp'),
    path('fires/', csrf_exempt(views.fires), name = 'allFires'),
    path('conditions/', csrf_exempt(views.actualState), name = 'actualState'),
    path('temperature/', csrf_exempt(views.temperature), name = 'temperature'),
    path('humidity/', csrf_exempt(views.humidity), name = 'humidity'),
    path('carbon/', csrf_exempt(views.carbon), name = 'carbon'),
    path('devices/', csrf_exempt(views.Devicesx), name = 'Devices'),



    ]
