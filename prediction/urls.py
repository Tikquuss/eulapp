from django.urls import path, include
from .views import home, about


urlpatterns = [
    path('' , home, name="home"),
    path('about' , about, name="about"),
    path('accounts/', include('django.contrib.auth.urls'), name="accounts"),
]