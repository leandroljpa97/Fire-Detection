from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name='users'

urlpatterns = [
	path('', csrf_exempt(views.login), name = 'loginUser'),
	path('signup/', csrf_exempt(views.signUp), name = 'signUp'),
    path('fires/', csrf_exempt(views.fires), name = 'allFires'),
    path('conditions/', csrf_exempt(views.actualState), name = 'actualState'),
    path('updateDevice/', csrf_exempt(views.DevicesUpd), name = 'DevicesUpdate'),
    path('devices/', csrf_exempt(views.ListAllDevices), name = 'DevicesAll'),
    path('fresh/', csrf_exempt(views.Fresh), name = 'Fresh'),
    path('sensors/', csrf_exempt(views.Uplink), name = 'Data'),
    path('mail/',csrf_exempt(views.saveMail), name = 'mail'),
    path('fire/',csrf_exempt(views.aux), name = 'fire'),



    ]
