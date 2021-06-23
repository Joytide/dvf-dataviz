"""DVF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
import dataviz.views as dataviz

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", dataviz.home),
    path("index", dataviz.home),
    path("graph_fi",dataviz.graph_fi),
    path("graph_terrain",dataviz.graph_terrain),
    path("graph_geo",dataviz.graph_geo),
    path("graph_comp",dataviz.graph_comp),
    path("graph_dyn_nature",dataviz.graph_dyn_nature),
    path("graph_dyn_evol_prix",dataviz.graph_dyn_evol_prix),
]
