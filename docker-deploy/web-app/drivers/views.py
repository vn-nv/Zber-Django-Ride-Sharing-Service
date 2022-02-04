from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.core.mail import send_mail
from django.db.models import Q

from .forms import DriverForm, SearchFormSet, SearchForm
from .models import Driver
import sys
sys.path.append("..")
from riders.models import Ride, Ride_Owner, Ride_Sharer

"""
   Index page of driver information
"""


@login_required
def index(request):
    drivers = Driver.objects.filter(user = request.user)
    if (drivers.exists()):
        driver = drivers.get()
        confirmed_rides = Ride.objects.filter(driver = driver, status='c')
        complete_rides = Ride.objects.filter(driver = driver, status='t')
    else:
        driver = None
        complete_rides = None
        confirmed_rides = None
    context = {'user': request.user,
               'driver': driver,
               'confirmed_rides': confirmed_rides,
               'complete_rides': complete_rides,
               }
    return render(request, 'drivers/index.html', context)


"""
   Register as a driver
"""


@login_required
def register(request):
    if request.method == 'POST':
        # create a driver and back to index page
        form = DriverForm(request.POST)
        if form.is_valid():
            new_driver = form.save(commit = False)
            new_driver.user = request.user
            new_driver.save()
            return redirect('zber:drivers:index')
    else:
        form = DriverForm()

    return render(request, 'drivers/register.html', {'form': form})


"""
   Edit driver information
"""

@login_required
def edit(request):
    if request.method == 'POST':        
        form = DriverForm(request.POST,
                          instance = Driver.objects.get(user = request.user))
        if form.is_valid():
            form.save()
            return redirect('zber:drivers:index')
    else:
        form = DriverForm(instance = Driver.objects.get(user = request.user))
    return render(request, 'drivers/edit.html', {'form' : form})

@login_required
def delete(request):
    if request.method == 'POST':
        driver = Driver.objects.get(user=request.user)
        # de-confirm all confirmed orders
        rides = Ride.objects.filter(status='c').filter(driver=driver)
        for ride in rides:
            ride.status='o'
            send_mail(
            'Confirmation Cancelled',
            'We are sorry to inform you that your confirmed order has been re-opened.',
            'zber568@outlook.com',
            [ride.ride_owner.user.email],
            fail_silently=False,
            )
            ride.save()
        driver.delete()
        return redirect('zber:drivers:index')
    else:
        return render(request, 'drivers/delete.html', {})    

"""
   Ride view in driver app
"""

@login_required
def ride(request, ride_owner_id):
    driver = Driver.objects.get(user = request.user)
    ride_owner = Ride_Owner.objects.get(order_no = ride_owner_id)
    ride = Ride.objects.get(ride_owner = ride_owner)    
    ride_sharers = Ride_Sharer.objects.filter(ride = ride)
    context = {'driver': driver,
               'ride': ride,
               'ride_owner': ride_owner,
               'ride_sharers': ride_sharers
               }
    return render(request, 'drivers/ride.html', context)


"""
   Completes a ride. Only allow POST request, raise 404 error for GET request
"""

@login_required
def ride_complete(request, ride_owner_id):
    if request.method == 'POST':
        ride_owner = Ride_Owner.objects.get(order_no = ride_owner_id)
        ride = Ride.objects.get(ride_owner = ride_owner)
        ride.status = 't'
        ride.save()
        return redirect('zber:drivers:index')
    else:
        raise Http404("Page Not Found")


    
"""
   Display all search results to driver user
"""

@login_required
def search(request):
    results = Ride.objects.filter(status='o')
    # exclude driver user requested rides
    results = results.exclude(ride_owner__user=request.user)    
    driver_shared_ride_owners = Ride_Sharer.objects.filter(user=request.user).values_list('ride__ride_owner', flat=True)
    # exclude all ride that shared by driver user
    results = results.exclude(ride_owner__in=driver_shared_ride_owners)
    driver = Driver.objects.get(user = request.user)
    results = results.filter(sum_passengers__range=(1, driver.max_passengers))
    results = results.filter(Q(ride_owner__specific_type='') | Q(ride_owner__specific_type=driver.vehicle_type))
    results = results.filter(Q(ride_owner__special_requests='') | Q(ride_owner__special_requests=driver.special_info))   

    context = {'result_rides': results}
    return render(request, 'drivers/search.html', context)


"""
   Confirm a ride
"""

@login_required
def ride_confirm(request, ride_owner_id):
    if request.method == 'POST':
        ride_owner = Ride_Owner.objects.get(order_no = ride_owner_id)
        ride = Ride.objects.get(ride_owner = ride_owner)
        ride.driver = Driver.objects.get(user = request.user)
        ride.status = 'c'
        # send email to owner and sharers, not sending to sharers yet
        send_mail(
            'Ride Confirmation',
            'This is a confirmation to let you know that your ride request has been confirmed!',
            'zber568@outlook.com',
            [ride.ride_owner.user.email],
            fail_silently=False,
        )
        ride.save()
        return redirect('zber:drivers:index')
    else:
        raise Http404("Page Not Found")
    
"""
   Cancel a ride, set the status back to open and reset the driver to null
"""

@login_required
def ride_cancel(request, ride_owner_id):
    if request.method == 'POST':
        ride_owner = Ride_Owner.objects.get(order_no = ride_owner_id)
        ride = Ride.objects.get(ride_owner = ride_owner)
        # reset driver to null
        ride.driver = None
        # reset status to open
        ride.status = 'o'
        # send email to owner and sharers, not sending to sharers yet
        send_mail(
            'Ride Cancellation',
            'This is to inform you that your confirmed ride has been cancelled!',
            'zber568@outlook.com',
            [ride.ride_owner.user.email],
            fail_silently=False,
        )
        ride.save()
        return redirect('zber:drivers:index')
    else:
        raise Http404("Page Not Found")
