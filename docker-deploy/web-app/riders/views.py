from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.urls import reverse
import sys
sys.path.append("..")
from .forms import DriverForm, RideForm, RideOwnerForm, SharerForm, UserForm
from .models import Ride, Ride_Owner, Ride_Sharer



@login_required
def getRideRequest(request):
    my_requests = Ride.objects.filter(status = 'o', ride_owner__user = request.user)
    shared_rides = Ride_Sharer.objects.filter(user=request.user, ride__status='o')
    my_shared_rides = []
    for shared_ride in shared_rides:
        my_shared_rides.append(shared_ride.ride)
    shares = Ride_Sharer.objects.filter(user = request.user).values_list('ride__ride_owner', flat=True)
    confirmed_shared_rides = Ride.objects.filter(status = 'c', share = True, ride_owner__in=shares)
    my_rides = Ride.objects.filter(status = 'c', ride_owner__user = request.user)
    context = {'my_requests': my_requests,
               'my_shared_rides': my_shared_rides,
               'my_rides': my_rides,
               'confirmed_shared_rides': confirmed_shared_rides
               }
    return render(request, 'riders/index.html', context)


@login_required
def getFullRide(request, ride_order_no):
    ride_owner = Ride_Owner.objects.filter(order_no = ride_order_no).get()
    ride = Ride.objects.filter(ride_owner__order_no = ride_order_no).get()
    ride_sharers = Ride_Sharer.objects.filter(ride = ride)
    sharers = []
    for ride_sharer in ride_sharers:
        sharers.append([ride_sharer.user, ride_sharer.sum_sharers])
    print(sharers)
    ride_owner_user_form = UserForm(instance=ride_owner.user)
    ride_owner_form = RideOwnerForm(instance=ride_owner)
    if ride.driver is not None and ride.driver != "":
        driver_form = DriverForm(instance=ride.driver)
        driver_user_form = UserForm(instance=ride.driver.user)
    else:
        driver_form = None
        driver_user_form = None
    ride_form = RideForm(instance=ride)
    context = {
        'ride_order_no': ride_order_no,
        'sharers': ride_sharers,
        'ride_owner': ride_owner,
        'ride':ride,
        'driver':ride.driver,  
        
    }
    return render(request, 'riders/getFullRide.html', context)


@login_required
def getOpenRide(request):
    excluded_shares = Ride_Sharer.objects.filter(user = request.user).values_list('ride__ride_owner', flat=True)
    ride_requests = Ride.objects.filter(status = 'o', share = True).exclude(ride_owner__in=excluded_shares).exclude(ride_owner__user = request.user)
    if request.method == 'POST':  
        sum_passengers = request.POST.get('sum_passengers')
        destination = request.POST.get('destination')
        early_arrival_time = request.POST.get('early_arrival_time')
        late_arrival_time = request.POST.get('late_arrival_time')
        if sum_passengers is not None and sum_passengers != "":
            ride_requests = ride_requests.filter(sum_passengers__lte = sum_passengers)
        if destination is not None and destination is not "":
            ride_requests = ride_requests.filter(dest_addr = destination)
        if early_arrival_time is not None and early_arrival_time is not "":
            ride_requests = ride_requests.filter(arrival_time__gte = early_arrival_time)
        if late_arrival_time is not None and late_arrival_time is not "":
            ride_requests = ride_requests.filter(arrival_time__lte = late_arrival_time)
    context = {'ride_requests': ride_requests}
    return render(request, 'riders/getOpenRide.html', context)


@login_required
def postRideRequest(request):
    if request.method == 'POST':
        ride_form = RideForm(request.POST)
        ride_owner_form = RideOwnerForm(request.POST)
        if ride_form.is_valid() and ride_owner_form.is_valid():
            new_ride = ride_form.save(commit=False)
            new_ride_owner = ride_owner_form.save(commit=False)
            new_ride_owner.user = request.user
            new_ride.sum_passengers = new_ride_owner.sum_owners
            new_ride.ride_owner = new_ride_owner
            new_ride.status = 'o'
            new_ride_owner.save()
            new_ride.save()
            return redirect('zber:riders:index')
    else:
        ride_form = RideForm()
        ride_owner_form = RideOwnerForm()

    return render(request, 'riders/postRideRequest.html', {'ride_form': ride_form, 'ride_owner_form': ride_owner_form})


"""
   Edit driver information
"""


@login_required
def editRideRequest(request, ride_order_no):
    my_request = Ride_Owner.objects.filter(order_no=ride_order_no).get()
    my_ride = Ride.objects.filter(ride_owner=my_request).get()
    if request.method == 'POST':
        ordinary_passengers = my_ride.sum_passengers
        ordinary_owners = my_request.sum_owners
        ride_form = RideForm(request.POST, instance=my_ride)
        ride_owner_form = RideOwnerForm(request.POST, instance=my_request)  
        if ride_form.is_valid() and ride_owner_form.is_valid():
            edit_ride = ride_form.save(commit=False)
            edit_ride_owner = ride_owner_form.save(commit=False)
            edit_ride.sum_passengers = ordinary_passengers - ordinary_owners + edit_ride_owner.sum_owners
            edit_ride_owner.save()
            edit_ride.save()
            return redirect('zber:riders:index')
    else:
        ride_form = RideForm(instance=my_ride)
        ride_owner_form = RideOwnerForm(instance=my_request)
    return render(request, 'riders/editRideRequest.html', {'ride_order_no': my_request.order_no, 'ride_form': ride_form, 'ride_owner_form': ride_owner_form})


"""
   Edit driver information
"""


@login_required
def deleteSharedRide(request, ride_order_no):
    if request.method == 'POST':  
        delete_shared_ride = Ride_Sharer.objects.filter(ride__ride_owner__order_no = ride_order_no, user = request.user).get()
        update_ride = Ride.objects.filter(ride_owner__order_no = ride_order_no).get()
        update_ride.sum_passengers = update_ride.sum_passengers - delete_shared_ride.sum_sharers
        update_ride.save()
        delete_shared_ride.delete()
    return redirect('zber:riders:index')


@login_required
def deleteRideRequest(request, ride_order_no):
    if request.method == 'POST':  
        delete_ride_owner = Ride_Owner.objects.filter(order_no = ride_order_no).get()
        delete_ride = Ride.objects.filter(ride_owner__order_no = ride_order_no).get()
        delete_ride.delete()
        delete_ride_owner.delete()
        delete_sharers = Ride_Sharer.objects.filter(ride__ride_owner__order_no = ride_order_no)
        for delete_share in delete_sharers:
            delete_share.delete()
    return redirect('zber:riders:index')


"""
   Ride view in driver app
"""


@login_required
def shareRide(request, ride_order_no):
    if request.method == 'POST':  
        share_ride = Ride.objects.filter(ride_owner__order_no=ride_order_no).get()
        sum_sharers = int(request.POST['sum_sharers'])
        sharer = SharerForm()
        ride_sharer = sharer.save(commit=False)
        ride_sharer.user = request.user
        ride_sharer.ride = share_ride
        ride_sharer.sum_sharers = sum_sharers
        ride_sharer.save()
        share_ride.sum_passengers = share_ride.sum_passengers + ride_sharer.sum_sharers
        share_ride.save()
    return redirect('zber:riders:index')


@login_required
def editSharedRide(request, ride_order_no):
    share_ride = Ride.objects.filter(ride_owner__order_no=ride_order_no).get()
    ride_sharer = Ride_Sharer.objects.filter(ride=share_ride, user=request.user).get()
    sharer = SharerForm(instance=ride_sharer)
    if request.method == 'POST':
        sum_sharers = int(request.POST['sum_sharers'])      
        share_ride.sum_passengers = share_ride.sum_passengers - ride_sharer.sum_sharers  + sum_sharers
        sharer = sharer.save(commit=False)
        sharer.sum_sharers = sum_sharers
        sharer.save()
        share_ride.save()
        return redirect('zber:riders:index')
    else:
        return render(request, 'riders/index.html', {'sum_sharers': sharer.sum_sharers})
