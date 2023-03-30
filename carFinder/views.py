from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def index(request):
	return render(request, "main/index.html")

def all_cars(request):
	cars = Car.objects.all()
	return render(request, "main/car_list.html", {'cars': cars})

def car_list(request):
	cars = Car.objects.filter(on_sale = True)
	return render(request, "main/car_list.html", {'cars': cars})

def brand_list(request):
	brands = Brand.objects.all()
	return render(request, "main/brand_list.html", {'brands': brands})

def model_list(request):
	models = Model.objects.all()
	return render(request, "main/model_list.html", {'models': models})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="main/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request, "Invalid username or password")
		else:
			messages.error(request, "Invalid username or password")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})