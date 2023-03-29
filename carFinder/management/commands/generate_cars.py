from django.core.management.base import BaseCommand
from faker import Faker
from carFinder.models import Brand, Model, Car
import random

class Command(BaseCommand):
  help = 'Generate random cars and add them to the database'

  def add_arguments(self, parser):
    parser.add_argument('count', type=int, help='Number of cars to generate')

  def handle(self, *args, **options):

    transmissions = ["manual", "automatic"]
    fuel_types = ["petrol", "diesel"]
    engine_types = ["2.0L", "1.4L", "3.0L", "5.0L"]
    brand_names = [
              "BMW", "Mercedec-Benz", "Audi", "Citroen",
              "Nissan", "Honda", "Mazda", "Hyundai",
              "Skoda", "Wolkswagen", "Renault", "Peugeot",
              "Toyota", "Aston Martin", "Daewoo", "Lexus",
              "Opel", "Mitsubishi", "Porshe", "Seat", "Suzuki",
              ]
    body_styles = ["sedan", "hatchback", "liftback", "coupe", "crossover", "wagon"]

    fake = Faker()
    count = options['count']

    for i in range(count):
      brand_name = random.choice(brand_names)
      country = fake.country()
    
      model_name = fake.random_letter() + str(fake.random_int())
      year = fake.random_int(1996, 2023)
      body_style = random.choice(body_styles)

      transmission = random.choice(transmissions)
      fuel_type = random.choice(fuel_types)
      mileage = fake.random_int()
      price = fake.random_int()
      extr_color = fake.color()
      intr_color = fake.color()
      engine_type = random.choice(engine_types)
      on_sale = fake.boolean()

      try:
        model = Model.objects.create(name=model_name, year=year, body_style=body_style)
      except:
        model = Model.objects.get(name = model_name)

      try:
        brand = Brand.objects.create(name=brand_name, country=country)
      except:
        brand = Brand.objects.get(name=brand_name)
        
      car = Car.objects.create(model=model, brand=brand, price=price, mileage=mileage, engine=engine_type, transmission=transmission, fuel_type=fuel_type, extr_color=extr_color, intr_color=intr_color, on_sale=on_sale)
      self.stdout.write(self.style.SUCCESS(f'Successfully created car {car}'))
