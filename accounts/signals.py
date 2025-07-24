from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Customer, Order

# Create Customer and assign to group
def customer_profile(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name="customer")
        instance.groups.add(group)
        Customer.objects.get_or_create(
            user=instance,
            defaults={'name': instance.username},
        )

# When a new Order is saved, check total purchase amount
@receiver(post_save, sender=Order)
def check_total_purchase_and_send_email(sender, instance, created, **kwargs):
    if created and instance.customer:
        total_amount = sum(order.product.price for order in instance.customer.order_set.all())
        recipient_email = instance.customer.email
        customer_name = instance.customer.name

        # Case 1: ₹2999 < total ≤ ₹5000 — Send 30% OFF email
        if 2999 < total_amount <= 5000:
            subject = "🎉 30% OFF on Your Next Purchase!"
            message = f"""
Hi {customer_name},

Great news!

You've spent over ₹2999 in total purchases with us.
As a reward, you’ve earned **30% OFF on your next order**!

Use code: SAVE30 at checkout.

Happy Shopping!  
— Team Diptayah
"""
            try:
                send_mail(
                    subject,
                    message,
                    "your@gmail.com",
                    [recipient_email],
                    fail_silently=False,
                )
            except Exception as e:
                print("Error sending 30% off email:", e)

        # Case 2: total > ₹5000 — Send Premium Reward email
        elif total_amount > 5000:
            subject = "🎉 You're Eligible for a Reward!"
            message = f"""
Hi {customer_name},

Thanks for shopping with us!

Your total purchase amount has now exceeded ₹5000.
You're now eligible for:
Free Delivery on your next order  
Exclusive Discount Coupons  

Happy Shopping!  
— Team Diptayah
"""
            try:
                send_mail(
                    subject,
                    message,
                    "your@gmail.com",
                    [recipient_email],
                    fail_silently=False,
                )
            except Exception as e:
                print("Error sending reward email:", e)

# Connect the signal
post_save.connect(customer_profile, sender=User)
