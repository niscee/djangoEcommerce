from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

#list of models
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, default=None)
    phone = models.CharField(max_length=200, default=None, null=True)

    

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    stock = models.IntegerField(default=1)

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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable = False, unique=True)
   

    def __str__(self):
        return str(self.transaction_id)
    
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-date_added']

    #getting total price of the single order item
    @property
    def get_totalPrice(self):
        total = self.product.price * self.quantity
        return total   

    def __str__(self):
        return str(self.order)              



class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    def __str__(self):
        return self.address

    



""" list of signals """
#initiatied whenever user creates a new account.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
     


# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# post_save.connect(create_profile, sender=User)  