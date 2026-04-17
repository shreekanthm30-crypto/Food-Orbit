from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length= 20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=80)

class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    picture = models.URLField(max_length=300, default="https://static.vecteezy.com/system/resources/previews/052/792/818/non_2x/restaurant-logo-design-vector.jpg")
    cuisine = models.CharField(max_length = 200)
    rating = models.FloatField()

class Item(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name = "items")
    name = models.CharField(max_length = 20)
    picture = models.URLField(max_length = 200, default="https://cdn-icons-png.flaticon.com/512/1147/1147856.png")
    description = models.CharField(max_length = 200)
    price = models.FloatField()
    is_veg = models.BooleanField(default = True)

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)


