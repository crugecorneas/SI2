"""
URL configuration for VotingProj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from votoAppWSServer.views import (aportarinfo_censo, aportarinfo_voto,
                           testbd, getvotos, delvoto)

from votoAppWSServer.views import CensoView, VotoView, ProcesoElectoralView
urlpatterns = [
    path("", aportarinfo_censo, name="index"),
    #path("censo/", aportarinfo_censo, name="censo"),
    #path("voto/", aportarinfo_voto, name="voto"),
    path("testbd/", testbd, name="testbd"),
    path("testbd/getvotos/", getvotos, name="getvotos"),
    path("testbd/delvoto/", delvoto, name="delvoto"),

    # check if person is in "censo"
    path('censo/', CensoView.as_view(), name='censo'),
    
    # create "voto"
    path('voto/', VotoView.as_view(), name='voto'),
    
    # get list of "votos" associated with a given idProcesoElectoral
    path('procesoelectoral/<str:idProcesoElectoral>/', ProcesoElectoralView.as_view(), name='procesoelectoral'),
    
    # delete "voto" with id id_voto
    path('voto/<str:id_voto>/', VotoView.as_view(), name='voto'),
]
