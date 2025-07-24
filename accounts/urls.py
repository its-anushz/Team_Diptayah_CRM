import logging  #Enables logging for debugging errors 

try:
    from django.urls import path
    from django.contrib.auth import views as auth_views
    from . import views
except ImportError as e:
    raise ImportError(f"Failed to import modules in urls.py: {e}")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

try:
    urlpatterns = [
        path('login/', views.loginPage, name="login"),
        path('logout/', views.logoutUser, name="logout"),
        path('register/', views.registerPage, name="register"),
        path('', views.home, name="home"),
        path('create_customer/', views.createCustomer, name='create_customer'),
        path('user/', views.user, name="user"),
        path('account/', views.accountSettings, name="account"),
        path('products/', views.products, name="products"),
        path('create_product/', views.createProduct, name='create_product'),
        path("update_product/<str:primary_key>/", views.updateProduct, name="update_product"),
        path("delete_product/<str:primary_key>/", views.deleteProduct, name="delete_product"),
        path('customers-by-bill/', views.customers_by_bill, name="customers_by_bill"),
        path('send-query-email/', views.send_query_email, name='send-query-email'),

        
        path('customer/<str:primary_key>/', views.customer, name="customer"),
        path('update_customer/<str:primary_key>/', views.updateCustomer, name="update_customer"),
        path('delete_customer/<str:primary_key>/', views.deleteCustomer, name="delete_customer"),
        path('create_order/<str:primary_key>/', views.createOrder, name="create_order"),
        path('update_order/<str:primary_key>/', views.updateOrder, name="update_order"),
        path('delete_order/<str:primary_key>/', views.deleteOrder, name="delete_order"),
        path(
            'reset_password/',
            auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
            name="reset_password"
        ),
        path(
            'reset_password_sent/',
            auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
            name="password_reset_done"
        ),
        path(
            'reset/<uidb64>/<token>/',
            auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
            name="password_reset_confirm"
        ),
        path(
            'reset_password_complete/',
            auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
            name="password_reset_complete"
        ),
    ]
except Exception as e:
    logger.exception(f"Error configuring URL patterns: {e}")
    urlpatterns = []
