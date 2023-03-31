from django.db import models

class Brand(models.Model):
	name = models.CharField(max_length = 50, unique = True)
	country = models.CharField(max_length = 80)

	def __str__(self):
		return self.name

class Model(models.Model):
	name = models.CharField(max_length = 80)
	year = models.IntegerField()
	body_style = models.CharField(max_length = 80)

	def __str__(self):
		return f"{self.name}, type: {self.body_style}"

class Car(models.Model):
	brand = models.ForeignKey(Brand, on_delete = models.CASCADE)
	model = models.ForeignKey(Model, on_delete = models.CASCADE)
	price = models.IntegerField()
	mileage = models.IntegerField()
	extr_color = models.CharField(max_length = 50)
	intr_color = models.CharField(max_length = 50)
	fuel_type = models.CharField(max_length = 50)
	transmission = models.CharField(max_length = 50)
	engine = models.CharField(max_length = 50)
	on_sale = models.BooleanField()
	
	def __str__(self):
		return f"{self.brand.name} {self.model.name}"
