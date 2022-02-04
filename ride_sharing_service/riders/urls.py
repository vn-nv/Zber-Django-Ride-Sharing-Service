from django.urls import path

from .import views

app_name = 'riders'
urlpatterns = [
     path("", views.getRideRequest, name = 'index'),
     path("getRideRequest", views.getRideRequest, name = 'getRideRequest'),
     path("postRideRequest", views.postRideRequest, name = 'postRideRequest'),
     path("getOpenRide", views.getOpenRide, name = 'getOpenRide'),
     path("<int:ride_order_no>/editRideRequest/", views.editRideRequest, name = 'editRideRequest'),
     path("<int:ride_order_no>/editSharedRide/", views.editSharedRide, name = 'editSharedRide'),
     path("editRideRequest", views.editRideRequest, name = 'editRideRequest'),
     path("getFullRide", views.getFullRide, name = 'getFullRide'),
     path("<int:ride_order_no>/getFullRide/",
         views.getFullRide,
         name='getFullRide'),
     path("<int:ride_order_no>/deleteRideRequest/",
          views.deleteRideRequest,
          name='deleteRideRequest'),
     path("<int:ride_order_no>/deleteSharedRide/",
         views.deleteSharedRide,
         name='deleteSharedRide'),
     path("<int:ride_order_no>/shareRide/",
          views.shareRide,
          name='shareRide'),
     path("getRideRequest/<int:order_no>", views.getRideRequest, name = 'ride'),
]
