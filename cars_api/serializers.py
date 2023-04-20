from rest_framework import serializers
from carFinder.models import Car, Brand, Model, Profile
from django.contrib.auth.models import User


class BrandSerializer(serializers.ModelSerializer):
	class Meta:
		model = Brand
		fields = ['name', 'country']


class CarModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Model
		fields = ['name', 'year', 'body_style']


class UserRegisterSerializer(serializers.ModelSerializer):
	password_confirmation = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'password_confirmation']

	def validate(self, data):
		password = data.get('password')
		password_confirmation = data.pop('password_confirmation')

		if password != password_confirmation:
			raise serializers.ValidationError('Passwords do not match')
		return data

	def create(self, validated_data):
		password = validated_data.pop('password')
		user = User(**validated_data)
		user.set_password(password)
		user.save()
		return user


class LoginSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'password']


class UserInfoSerializer(serializers.ModelSerializer):
	username = serializers.CharField(required=False)

	class Meta:
		model = User
		fields = ['username', 'email']


class CarSerializer(serializers.ModelSerializer):
	model = CarModelSerializer()
	owner = UserInfoSerializer(read_only=True)

	class Meta:
		model = Car
		fields = [
			'id', 'brand', 'model',
			'price', 'mileage', 'extr_color',
			'intr_color', 'fuel_type',
			'transmission', 'engine', 'on_sale', 'owner'
		]
		read_only_fields = ['id']

	def create(self, validated_data):
		model_data = validated_data.pop('model')
		model = Model.objects.create(**model_data)
		validated_data['model'] = model
		owner = self.context['request'].user
		validated_data['owner'] = owner
		car = Car.objects.create(**validated_data)
		car.save()
		return car

	def update(self, instance, validated_data):
		print(validated_data)
		model_data = validated_data.pop('model')
		existed_model = Model.objects.filter(
			name=model_data['name'],
			year=model_data['year'],
			body_style=model_data['body_style']
		).first()
		if not existed_model:
			model = Model.objects.create(**model_data)
		else:
			model = existed_model
		instance.model = model
		instance.brand = validated_data.get('brand', instance.brand_id)
		instance.price = validated_data.get('price', instance.price)
		instance.mileage = validated_data.get('mileage', instance.mileage)
		instance.extr_color = validated_data.get('extr_color', instance.extr_color)
		instance.intr_color = validated_data.get('intr_color', instance.intr_color)
		instance.fuel_type = validated_data.get('fuel_type', instance.fuel_type)
		instance.transmission = validated_data.get('transmission', instance.transmission)
		instance.engine = validated_data.get('engine', instance.engine)
		instance.on_sale = validated_data.get('on_sale', instance.on_sale)
		instance.save()
		return instance


class ProfileSerializer(serializers.ModelSerializer):
	user = UserInfoSerializer(many=False)
	favorite_cars = CarSerializer(many=True)
	owned_cars = serializers.SerializerMethodField()

	class Meta:
		model = Profile
		fields = ['user', 'phone_number', 'home_address', 'favorite_cars', 'owned_cars']
		read_only_fields = ['favorite_cars']

	def update(self, instance, validated_data):
		user_data = validated_data.pop('user')
		user = instance.user
		instance.phone_number = validated_data.get('phone_number', instance.phone_number)
		instance.home_address = validated_data.get('home_address', instance.home_address)
		instance.save()
		user.username = user_data.get('username', user.username)
		user.email = user_data.get('email', user.email)
		user.save()
		return instance

	def validate_user(self, value):
		if not value.get('username'):
			raise serializers.ValidationError({'username': 'Username can`t be blank'})
		if self.instance and value.get('username') == self.instance.user.username:
			return value
		if User.objects.filter(username=value.get('username', self.instance.user.username)).exists():
			raise serializers.ValidationError({'username': 'A user with that username already exists'})
		temp = False
		special_symbols = ['@', '.', '+', '-', '_']
		for char in value['username']:
			if char.isdigit() or char.isalpha() or char in special_symbols:
				continue
			temp = True
			break
		if len(value['username']) > 150 or temp:
			raise serializers.ValidationError({'username': 'Incorrect username'})
		return value

	@staticmethod
	def get_owned_cars(obj):
		cars = obj.user.cars.all().select_related("model", "owner")
		return {
			"cars": CarSerializer(cars, many=True).data,
			"total": cars.count()
		}