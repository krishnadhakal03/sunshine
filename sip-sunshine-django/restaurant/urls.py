from django.urls import path
from django.views.generic import TemplateView
from . import views, api
from .checkout_views import CheckoutView, OrderConfirmationView, OrderTrackingView, CreateOrderView

app_name = 'restaurant'

urlpatterns = [
    # Pages
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('menu/', views.MenuPageView.as_view(), name='menu'),
    path('terms/', TemplateView.as_view(template_name='pages/terms.html'), name='terms'),
    path('privacy/', TemplateView.as_view(template_name='pages/privacy.html'), name='privacy'),
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('reservation/', views.ReservationView.as_view(), name='reservation'),
    path('page/<slug:slug>/', views.PageView.as_view(), name='page'),
    
    # Customer Authentication
    path('auth/register/', views.CustomerRegisterView.as_view(), name='customer_register'),
    path('auth/login/', views.CustomerLoginView.as_view(), name='customer_login'),
    path('auth/logout/', views.CustomerLogoutView.as_view(), name='customer_logout'),
    path('auth/profile/', views.CustomerProfileView.as_view(), name='customer_profile'),
    
    # Orders & Checkout
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/create/', CreateOrderView.as_view(), name='create_order'),
    path('orders/confirmation/<int:order_id>/', OrderConfirmationView.as_view(), name='order_confirmation'),
    path('orders/tracking/', OrderTrackingView.as_view(), name='order_tracking'),
    
    # API Endpoints
    path('api/settings/delivery/', api.get_delivery_settings, name='api_delivery_settings'),
    path('api/orders/create/', api.create_order, name='api_create_order'),
    path('api/orders/<int:order_id>/', api.get_order_status, name='api_order_status'),
    path('api/chatbot/', api.chatbot_message, name='api_chatbot'),
]
