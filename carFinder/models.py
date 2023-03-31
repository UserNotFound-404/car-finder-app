from django.db import models
import colorsys


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
	
	def get_hsl_color(color):
		temp_rgb = tuple(int(color[i:i+2], 16) for i in (1,3,5))
		return colorsys.rgb_to_hls(*[c/255.0 for c in temp_rgb])

	def get_color_distance(color1, color2):
		return float(((color1[0] - color2[0])**2 + (color1[1] - color2[1])**2 + (color1[2] - color2[2])**2) ** 0.5)

	def __str__(self):
		return f"{self.brand.name} {self.model.name}"
