from django.contrib.auth.models import User
from django.db import models


class Brand(models.Model):
	name = models.CharField(max_length=50, unique=True)
	country = models.CharField(max_length=80)

	def __str__(self):
		return self.name


class Model(models.Model):
	name = models.CharField(max_length=80)
	year = models.IntegerField()
	body_style = models.CharField(max_length=80)

	def __str__(self):
		return f"{self.name}, type: {self.body_style}"


class Car(models.Model):
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
	model = models.ForeignKey(Model, on_delete=models.CASCADE)
	price = models.IntegerField()
	mileage = models.IntegerField()
	extr_color = models.CharField(max_length=50)
	intr_color = models.CharField(max_length=50)
	fuel_type = models.CharField(max_length=50)
	transmission = models.CharField(max_length=50)
	engine = models.CharField(max_length=50)
	on_sale = models.BooleanField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cars", default=1)

	def __str__(self):
		return f"{self.brand.name} {self.model.name}"


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_account")
	phone_number = models.CharField(max_length=50, blank=True)
	home_address = models.TextField(max_length=250, blank=True)
	favorite_cars = models.ManyToManyField(Car, related_name="favorite_cars", blank=True, null=True)

	def __str__(self):
		return self.user.username

