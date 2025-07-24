from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import logging

logger = logging.getLogger(__name__)

# ***(1)Returns all customers from customer table
try:
    customers = Customer.objects.all()
except Exception as e:
    logger.exception(f"Error fetching all customers: {e}")
    customers = []

# (2)Returns first customer in table
firstCustomer = Customer.objects.first()

# (3)Returns last customer in table
lastCustomer = Customer.objects.last()

# (4)Returns single customer by name
try:
    customerByName = Customer.objects.get(name='Peter Piper')
except ObjectDoesNotExist:
    logger.warning("Customer with name 'Peter Piper' does not exist.")
    customerByName = None
except MultipleObjectsReturned:
    logger.warning("Multiple customers found with name 'Peter Piper'.")
    customerByName = Customer.objects.filter(name='Peter Piper').first()

# ***(5)Returns single customer by ID
try:
    customerById = Customer.objects.get(id=4)
except ObjectDoesNotExist:
    logger.warning("Customer with ID 4 does not exist.")
    customerById = None

# ***(6)Returns all orders related to customer (firstCustomer variable set above)
if firstCustomer:
    firstCustomerOrders = firstCustomer.order_set.all()
else:
    firstCustomerOrders = []

# (7)***Returns orders customer name: (Query parent model values)
order = Order.objects.first()
parentName = order.customer.name if order and order.customer else None

# (8)***Returns products from products table with value of "Out Door" in category attribute
products = Product.objects.filter(category="Out Door")

# (9)***Order/Sort Objects by id
leastToGreatest = Product.objects.all().order_by('id')
greatestToLeast = Product.objects.all().order_by('-id')

# (10)Returns all products with tag of "Sports": (Query Many to Many Fields)
productsFiltered = Product.objects.filter(tag__name="Sports")

'''
(11)Bonus
Q: If the customer has more than 1 ball, how would you reflect it in the database?
A: Because there are many different products and this value changes constantly you would most 
likly not want to store the value in the database but rather just make this a function we can run
each time we load the customers profile
'''

# Returns the total count for number of time a "Ball" was ordered by the first customer
if firstCustomer:
    ballOrders = firstCustomer.order_set.filter(product__name="Ball").count()
else:
    ballOrders = 0

# Returns total count for each product ordered
allOrders = {}

if firstCustomer:
    for order in firstCustomer.order_set.all():
        product_name = order.product.name if order.product else 'Unknown'
        if product_name in allOrders:
            allOrders[product_name] += 1
        else:
            allOrders[product_name] = 1

# Returns: allOrders: {'Ball': 2, 'BBQ Grill': 1}

# RELATED SET EXAMPLE
class ParentModel(models.Model):
    name = models.CharField(max_length=200, null=True)

class ChildModel(models.Model):
    parent = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)

parent = ParentModel.objects.first()
# Returns all child models related to parent
children = parent.childmodel_set.all() if parent else []
