from django.urls import path
from .views import app_scope, home, about, prediction, prediction_interface

urlpatterns = [
    path('' , home, name="home"),
    path('about' , about, name="about"),
    path('prediction' , prediction, name="prediction"),
    path('prediction_interface', prediction_interface, name = "prediction_interface"),
    path('app_scope', app_scope, name='app_scope'),
    path('a', app_scope, name='a'),
]