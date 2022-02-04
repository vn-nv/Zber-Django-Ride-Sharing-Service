from django.urls import path, include

from . import views
from drivers import urls as drivers_urls

app_name = 'app'
urlpatterns = [
    path("", views.index, name = 'index'),
    path("register", views.log_up, name = 'logup'),
    path("drivers/", include(drivers_urls, namespace = 'drivers')),
]
    
