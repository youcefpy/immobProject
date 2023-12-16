
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from immobApp import views
from django.shortcuts import render


urlpatterns = [
    path('',views.main_view,name="main_view"),
    path('admin/', admin.site.urls),
    path('inscription_visiteur/',views.inscription,name = "inscription_visiteur"),
    path('Exposant/',views.inscriptionExposant,name="Exposant"),
    path('apropos/',lambda request : render(request,'about.html'),name="about"),
    path('conatct/',views.conatct,name='contact'),

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)