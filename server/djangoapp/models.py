from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.timezone import now


# Create your models here.

# Create a Car Make model `class CarMake(models.Model)`:
class CarMake(models.Model):
    # - Name
    # - Description
    # - Any other fields you would like to include in car make model
    name = models.CharField(null=False, max_length=25)
    description = models.TextField(max_length=500)
    country = models.CharField(null=False, max_length=25)
    luxury = models.BooleanField(default=False)

    # - __str__ method to print a car make object
    def __str__(self):
        return "Brand Name: " + self.name

# Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    # - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    # - Name
    # - Dealer id, used to refer a dealer created in cloudant database
    # - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    # - Year (DateField)
    # - Any other fields you would like to include in car model
    brand = models.ForeignKey(CarMake, on_delete = models.CASCADE)
    name = models.CharField(null=False, max_length=25)
    dealerId = models.IntegerField(null=False)

    #Type Choices
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    COUPE = 'coupe'
    MINIVAN = 'minivan'
    CONVERTABLE = 'convertable'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Station Wagon'),
        (COUPE, 'Coupe'),
        (MINIVAN, 'Minivan'),
        (CONVERTABLE, 'Convertable')
    ]
    type = models.CharField(null=False, max_length=20, choices=TYPE_CHOICES, default=SEDAN)
    year = models.DateField(null=False)

    # - __str__ method to print a car make object
    def __str__(self):
        return "Model Name: " + self.name + "," + \
            "Year: " + str(self.year)

# Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment # positive, neutral or negative
        self.id = id

    def __str__(self):
        return "Dealer review: " + self.review