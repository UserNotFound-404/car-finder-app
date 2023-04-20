from django.contrib import admin
from .models import *
from django import forms


class CarForm(forms.ModelForm):
	class Meta:
		model = Car
		fields = '__all__'
		widgets = {
				'extr_color': forms.TextInput(attrs={'type': 'color'}),
				'intr_color': forms.TextInput(attrs={'type': 'color'}),
		}


class CarAdmin(admin.ModelAdmin):
	form = CarForm


admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(Car, CarAdmin)
admin.site.register(Profile)
