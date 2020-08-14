from django.db import models
from django.contrib.auth.models import User

# list of models
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    """ prevent getting error when no image is associated to product """
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url    



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.customer)
    
    #getting the total cost of cart Items
    @property
    def get_cartTotalPrice(self):
        orderitems = self.orderitem_set.all()
        totalPrice = sum([item.get_totalPrice for item in orderitems])
        return totalPrice   
    
    #getting total nuber of items in cart
    @property
    def get_cartTotalItems(self):
        orderitems = self.orderitem_set.all()
        totalItems = sum([item.quantity for item in orderitems])
        return totalItems        


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)   

    # def __str__(self):
    #      return self.order.transaction_id

    #getting total price of the single order item
    @property
    def get_totalPrice(self):
        total = self.product.price * self.quantity
        return total    



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    def __str__(self):
        return self.address


