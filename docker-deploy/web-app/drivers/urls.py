from django.urls import path

from .import views

app_name = 'drivers'
urlpatterns = [
    path("", views.index, name = 'index'),
    path("register", views.register, name = 'register'),
    path("edit", views.edit, name = 'edit'),
    path("delete", views.delete, name = 'delete'),
    path("ride/<int:ride_owner_id>", views.ride, name = 'ride'),
    path("ride/<int:ride_owner_id>/complete",
         views.ride_complete,
         name='ride_complete'),
    path("ride/<int:ride_owner_id>/confirm",
         views.ride_confirm,
         name='ride_confirm'),
    path("ride/<int:ride_owner_id>/cancel",
         views.ride_cancel,
         name='ride_cancel'),
    path("search", views.search, name = 'search'),
]
