from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def index(request):
	return render(request, "main/index.html")

def all_cars(request):
	cars = Car.objects.all()
	return render(request, "main/car_list.html", {'cars': cars})

def get_model_filter(request):
	model_name = request.GET.get('model')
	max_year = request.GET.get('max_year')
	min_year = request.GET.get('min_year')
	model_style = request.GET.get('model_style')
	return model_name, max_year, min_year, model_style

def get_brand_filter(request):
	brand_name = request.GET.get('brand')
	brand_country = request.GET.get('country')
	return brand_name, brand_country

def car_list(request):
	cars = Car.objects.filter(on_sale = True)
	filter_form = CarFilterForm(request.GET or None)

	brand_name, brand_country = get_brand_filter(request)
	model_name, max_year, min_year, model_style = get_model_filter(request)

	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')
	min_mileage = request.GET.get('min_mileage')
	max_mileage = request.GET.get('max_mileage')
	extr_color = request.GET.get('extr_color')
	intr_color = request.GET.get('intr_color')
	fuel_type = request.GET.get('fuel_type')
	selected_intr_color = request.GET.get('select_intr_color')
	selected_extr_color = request.GET.get('select_extr_color')
	if filter_form.is_valid():
		if brand_name:
			cars = cars.filter(brand__name=brand_name)
		if brand_country:
			cars = cars.filter(brand__country=brand_country)

		if model_name:
			cars = cars.filter(model__name=model_name)
		if max_year:
			cars = cars.filter(model__year__lte=max_year)
		if min_year:
			cars = cars.filter(model__year__gte=min_year)
		if model_style:
			cars = cars.filter(model__body_style=model_style)

		if min_price:
			cars = cars.filter(price__gte=min_price)
		if max_price:
			cars = cars.filter(price__lte=max_price)
		if min_mileage:
			cars = cars.filter(mileage__gte=min_mileage)
		if max_mileage:
			cars = cars.filter(mileage__lte=max_mileage)
		if extr_color and selected_extr_color:
			temp_car_list = cars
			extr_color_hsl = Car.get_hsl_color(extr_color)
			for car in temp_car_list:
				car_extr_hsl_color = Car.get_hsl_color(car.extr_color)
				distance = Car.get_color_distance(car_extr_hsl_color, extr_color_hsl)
				if distance > 0.21 and car in cars:
					cars = cars.exclude(id=car.id)
		if intr_color and selected_intr_color:
			temp_car_list = cars
			intr_color_hsl = Car.get_hsl_color(intr_color)
			for car in temp_car_list:
				car_intr_hsl_color = Car.get_hsl_color(car.intr_color)
				distance = Car.get_color_distance(car_intr_hsl_color, intr_color_hsl)
				if distance > 0.21 and car in cars:
					cars = cars.exclude(id=car.id)
		if fuel_type:
			cars = cars.filter(fuel_type=fuel_type)
	return render(request, 'main/car_list.html', {'cars': cars, 'filter_form': filter_form})

def brand_list(request):
	brands = Brand.objects.all()
	filter_form = BrandFilterForm(request.GET or None)
	brand_name, brand_country = get_brand_filter(request)
	if filter_form.is_valid():
		if brand_name:
			brands = brands.filter(name=brand_name)
		if brand_country:
			brands = brands.filter(country=brand_country)
	return render(request, "main/brand_list.html", {'brands': brands, 'filter_form': filter_form})

def model_list(request):
	models = Model.objects.all()
	filter_form = ModelFilterForm(request.GET or None)
	model_name, max_year, min_year, model_style = get_model_filter(request)
	if filter_form.is_valid():
		if model_name:
			models = models.filter(name=model_name)
		if max_year:
			models = models.filter(year__lte=max_year)
		if min_year:
			models = models.filter(year__gte=min_year)
		if model_style:
			models = models.filter(body_style=model_style)
	return render(request, "main/model_list.html", {'models': models, 'filter_form': filter_form})

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