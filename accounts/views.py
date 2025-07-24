from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError, PermissionDenied
from django.db import IntegrityError
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm, ProductForm
from .filters import OrderFilter
from .decorators import allowed_users, unauthenticated_user, admin_only



@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    try:
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get("username")
                messages.success(request, f"Account was created for {username}")
                return redirect("login")
    except ValidationError as e:
        messages.error(request, f"Validation error: {e}")
    except IntegrityError as e:
        messages.error(request, f"Integrity error: {e}")
    context = {"form": form}
    return render(request, "accounts/register.html", context)

@unauthenticated_user
def loginPage(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Username or Password is incorrect!")
    except Exception as e:
        messages.error(request, f"Login error: {str(e)}")
    return render(request, "accounts/login.html")

def logoutUser(request):
    logout(request)
    return redirect("login")

@login_required(login_url='login')
@allowed_users(allowed_roles=["customer"])
def user(request):
    try:
        orders = request.user.customer.order_set.all()
        total_orders = orders.count()
        orders_delivered = orders.filter(status="Delivered").count()
        orders_pending = orders.filter(status="Pending").count()
        context = {
            "orders": orders,
            "total_orders": total_orders,
            "orders_delivered": orders_delivered,
            "orders_pending": orders_pending,
        }
        return render(request, "accounts/user.html", context)
    except ObjectDoesNotExist:
        raise Http404("Customer data not found")

@login_required(login_url='login')
@allowed_users(allowed_roles=["customer"])
def accountSettings(request):
    try:
        customer = request.user.customer
        form = CustomerForm(instance=customer)
        if request.method == "POST":
            form = CustomerForm(request.POST, request.FILES, instance=customer)
            if form.is_valid():
                form.save()
        return render(request, 'accounts/account_settings.html', {"form": form})
    except ObjectDoesNotExist:
        raise Http404("Customer profile not found")
    except ValidationError as e:
        messages.error(request, f"Validation error: {e}")

from django.db.models import Sum, F, FloatField  # Make sure these are imported

@login_required(login_url='login')
@admin_only
def home(request):
    try:
        orders = Order.objects.all()

        # Annotate each customer with total bill (sum of their product prices)
        customers = Customer.objects.annotate(
            total_bill=Sum(F("order__product__price"), output_field=FloatField())
        ).order_by("-total_bill")  # Sorted by decending total bill

        context = {
            "orders": orders,
            "customers": customers,
            "total_orders": orders.count(),
            "orders_delivered": orders.filter(status="Delivered").count(),
            "orders_pending": orders.filter(status="Pending").count(),
        }
        return render(request, "accounts/dashboard.html", context)
    except Exception as e:
        return HttpResponse(f"Error loading dashboard: {str(e)}")


@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def products(request):
    try:
        products = Product.objects.all()
        return render(request, "accounts/products.html", {"products": products})
    except Exception as e:
        return HttpResponse(f"Error loading products: {str(e)}")


@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def createCustomer(request):
    try:
        form = CustomerForm()
        if request.method == 'POST':
            form = CustomerForm(request.POST, request.FILES)
            if form.is_valid():
                customer = form.save()
                logger.info(f"Customer created: {customer}")
                messages.success(request, "Customer created successfully.")
                return redirect('home')
            else:
                logger.warning(f"Invalid form: {form.errors}")
                messages.error(request, "Form is invalid. Please check the fields.")
        
        return render(request, 'accounts/create_customer.html', {'form': form})

    except Exception as e:
        logger.exception(f"Error in createCustomer view: {e}")
        return HttpResponse("An unexpected error occurred while creating the customer.", status=500)

@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def updateCustomer(request, primary_key):
    try:
        customer = Customer.objects.get(id=primary_key)
        form = CustomerForm(instance=customer)

        if request.method == "POST":
            form = CustomerForm(request.POST, request.FILES, instance=customer)
            if form.is_valid():
                form.save()
                return redirect("home")  # or wherever you want to redirect

        return render(request, 'accounts/customer_form.html', {'form': form})
    except Customer.DoesNotExist:
        return HttpResponse("Customer not found", status=404)

@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def deleteCustomer(request, primary_key):
    try:
        customer = Customer.objects.get(id=primary_key)
        if request.method == "POST":
            customer.delete()
            return redirect("home")
        return render(request, "accounts/delete_customer.html", {"item": customer})
    except Customer.DoesNotExist:
        raise Http404("Customer not found")


@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def customer(request, primary_key):
    try:
        customer = Customer.objects.get(id=primary_key)
        orders = customer.order_set.all()
        filter = OrderFilter(request.GET, queryset=orders)
        context = {
            "customer": customer,
            "orders": filter.qs,
            "order_count": orders.count(),
            "filter": filter,
        }
        return render(request, "accounts/customer.html", context)
    except Customer.DoesNotExist:
        raise Http404("Customer not found")

@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def createOrder(request, primary_key):
    try:
        OrderFormSet = inlineformset_factory(Customer, Order, fields=("product", "status"), extra=5)
        customer = Customer.objects.get(id=primary_key)
        formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

        if request.method == "POST":
            formset = OrderFormSet(request.POST, instance=customer)
            if formset.is_valid():
                formset.save()
                return redirect(f"/customer/{customer.id}")

        return render(request, "accounts/create_order.html", {"formset": formset})
    except Customer.DoesNotExist:
        raise Http404("Customer not found")


@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def updateOrder(request, primary_key):
    try:
        order = Order.objects.get(id=primary_key)
        form = OrderForm(instance=order)

        if request.method == "POST":
            form = OrderForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect(f'/customer/{order.customer.id}')

        return render(request, "accounts/update_order.html", {"form": form})
    except Order.DoesNotExist:
        raise Http404("Order not found")


@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def deleteOrder(request, primary_key):
    try:
        order = Order.objects.get(id=primary_key)
        if request.method == "POST":
            order.delete()
            return redirect("/")
        return render(request, "accounts/delete_order.html", {"item": order})
    except Order.DoesNotExist:
        raise Http404("Order not found")

@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def createProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')  # or redirect where appropriate
    return render(request, 'accounts/product_form.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def updateProduct(request, primary_key):
    try:
        product = get_object_or_404(Product, id=primary_key)
        form = ProductForm(instance=product)

        if request.method == "POST":
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "Product updated successfully.")
                return redirect("products")

        return render(request, "accounts/product_form.html", {"form": form})

    except Exception as e:
        logger.exception(f"Error in updateProduct view: {e}")
        return HttpResponse("An unexpected error occurred while updating the product.", status=500)


@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def deleteProduct(request, primary_key):
    try:
        product = get_object_or_404(Product, id=primary_key)

        if request.method == "POST":
            product.delete()
            messages.success(request, "Product deleted successfully.")
            return redirect("products")

        return render(request, "accounts/delete_product.html", {"item": product})

    except Exception as e:
        logger.exception(f"Error in deleteProduct view: {e}")
        return HttpResponse("An unexpected error occurred while deleting the product.", status=500)
    
from django.db.models import Sum, F, FloatField

@login_required(login_url='login')
@allowed_users(allowed_roles=["admin"])
def customers_by_bill(request):
    try:
        # Annotate each customer with total bill: sum of (order.product.price)
        customers = Customer.objects.annotate(
            total_bill=Sum(F("order__product__price"), output_field=FloatField())
        ).order_by("total_bill")  # Ascending order

        context = {
            "customers": customers,
        }
        return render(request, "accounts/customers_by_bill.html", context)
    except Exception as e:
        logger.exception(f"Error loading customers by bill: {e}")
        return HttpResponse("An error occurred while processing the customers.", status=500)


from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users

@login_required(login_url='login')
@allowed_users(allowed_roles=["customer"])
def send_query_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        customer_email = request.user.email

        if subject and message:
            try:
                full_message = f"Message from {request.user.username} ({customer_email}):\n\n{message}"
                send_mail(
                    subject,
                    full_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['channambhikas@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, "Your query has been sent to the admin.")
                return redirect('user')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            except Exception as e:
                return HttpResponse(f"Error sending mail: {str(e)}")
        else:
            messages.error(request, "Please enter a subject and message before sending.")
            return redirect('user')
    return redirect('user')

