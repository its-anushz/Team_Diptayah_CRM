from django.contrib import admin
import logging

logger = logging.getLogger(__name__)

try:
    from .models import Customer, Product, Tag, Order

    admin.site.register(Customer)
    admin.site.register(Product)
    admin.site.register(Tag)
    admin.site.register(Order)

except ImportError as e:
    logger.error(f"ImportError in admin.py: {e}")
    raise e
except AttributeError as e:
    logger.error(f"AttributeError in admin.py: {e}")
    raise e
except Exception as e:
    logger.exception(f"Unexpected error in admin.py: {e}")
    raise e
