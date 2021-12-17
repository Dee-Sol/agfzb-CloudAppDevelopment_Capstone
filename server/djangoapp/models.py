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

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
