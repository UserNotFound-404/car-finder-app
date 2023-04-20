from django_filters import rest_framework as filters
from carFinder.models import Car, Brand, Model
import colorsys


class CarFilter(filters.FilterSet):
	brand__name = filters.CharFilter(lookup_expr='icontains')
	brand__country = filters.CharFilter(lookup_expr='icontains')
	model__name = filters.CharFilter(lookup_expr='icontains')
	model__year = filters.NumberFilter(lookup_expr='icontains')
	model__body_style = filters.CharFilter(lookup_expr='icontains')
	min_year = filters.NumberFilter(field_name='model__year', lookup_expr='gte')
	max_year = filters.NumberFilter(field_name='model__year', lookup_expr='lte')
	max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
	min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
	extr_color = filters.CharFilter(field_name='extr_color', method='filter_color_similarity')
	intr_color = filters.CharFilter(field_name='intr_color', method='filter_color_similarity')

	@staticmethod
	def get_hsl_color(color):
		temp_rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
		return colorsys.rgb_to_hls(*[c/255.0 for c in temp_rgb])

	@staticmethod
	def get_color_distance(color1, color2):
		return float(((color1[0] - color2[0])**2 + (color1[1] - color2[1])**2 + (color1[2] - color2[2])**2) ** 0.5)

	def filter_color_similarity(self, queryset, name, value):
		value = '#' + value
		if len(value) != 7:
			return queryset
		current_hsl_color = self.get_hsl_color(value)
		for car in queryset:
			if name == 'extr_color':
				car_color_hsl = self.get_hsl_color(car.extr_color)
			else:
				car_color_hsl = self.get_hsl_color(car.intr_color)
			color_distance = self.get_color_distance(current_hsl_color, car_color_hsl)
			if color_distance > 0.22:
				queryset = queryset.exclude(pk=car.pk)
		return queryset

	class Meta:
		model = Car
		fields = [
			'brand', 'model', 'price', 'mileage',
			'extr_color', 'intr_color', 'fuel_type',
			'transmission', 'engine', 'on_sale',
			'min_price', 'max_price', 'max_year',
			'min_year',
		]


class BrandFilter(filters.FilterSet):
	class Meta:
		model = Brand
		fields = [
			'name', 'country'
		]


class ModelFilter(filters.FilterSet):
	class Meta:
		model = Model
		fields = [
			'name', 'year', 'body_style',
		]