from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.core.mail import send_mail

@login_required
def index(request):
    return redirect("home/")
