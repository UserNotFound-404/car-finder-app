from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def index(request):
	cars = Car.objects.all()
	return render(request, "main/index.html", {'cars': cars})
