from django.urls import path
from .views import home, about, prediction

urlpatterns = [
    path('' , home, name="home"),
    path('about' , about, name="about"),
    path('prediction' , prediction, name="prediction"),
]