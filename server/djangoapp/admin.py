from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
#    inlines = [CarModelInline]
    list_display = ('name', 'year')
    list_filter = ['name', 'type', 'year']
    search_fields = ['name', 'type', 'year']

# CarMakeAdmin class
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name', 'description']

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)