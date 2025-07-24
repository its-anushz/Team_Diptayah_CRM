from django.db import models, IntegrityError
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
import logging
from django.db import models
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

# Signal for creating customer profile
def customer_profile(sender, instance, created, **kwargs):
    try:
        if created:
            group, _ = Group.objects.get_or_create(name="customer")
            instance.groups.add(group)
            Customer.objects.get_or_create(
                user=instance,
                defaults={'name': instance.username},
            )
    except IntegrityError as e:
        logger.error(f"IntegrityError in customer_profile: {e}")
    except AttributeError as e:
        logger.error(f"AttributeError in customer_profile: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error in customer_profile: {e}")

post_save.connect(customer_profile, sender=User)

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="default.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def orders(self):
        try:
            order_count = self.order_set.all().count()
            return str(order_count)
        except AttributeError as e:
            logger.warning(f"AttributeError in Customer.orders: {e}")
            return "0"

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Tag"

class Product(models.Model):
    CATEGORY = (
        ("Sports", "Sports"),
        ("Formal Attire", "Formal Attire"),
        ("Traditional Clothing", "Traditional Clothing"),
        ("Kids Wear", "Kids Wear"),
        ("Men's fashion", "Men's fashion"),
        ("Women's fashion", "Women's fashion"),
        ("Out Door", "Out Door"),
        ("In Door", "In Door"),
        ("Home Decor", "Home Decor"),
        ("Beauty Products", "Beauty Products"),
    
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name if self.name else "Unnamed Product"

class Order(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Out for Delivery", "Out for Delivery"),
        ("Delivered", "Delivered"),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)

    def __str__(self):
        try:
            return self.product.name
        except AttributeError:
            return "Order with missing product"
class CustomerQuery(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.subject}"