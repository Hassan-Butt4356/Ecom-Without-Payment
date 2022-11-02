from django.contrib import admin
from django.urls import path, include
from store.views import (register, home, Home,
                         add_to_cart, remove_from_cart,
                         Order_Summary, remove_single_item_from_cart,
                         add_single_to_cart, Checkout, search,
                         )
from django.contrib.auth.views import LoginView, LogoutView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', include('store.api.urls', namespace='api')),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('', Home.as_view(), name='home'),
    path('order_summary/', Order_Summary.as_view(), name='order-summary'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('add_to_cart/<id>/', add_to_cart, name='add-to-cart'),
    path('add_single_to_cart/<id>/', add_single_to_cart, name='add-single-to-cart'),
    path('remove_single_item/<id>/', remove_single_item_from_cart, name='remove-single-item'),
    path('remove_from_cart/<id>/', remove_from_cart, name='remove-from-cart'),
    path('login/', LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='store/logout.html'), name='logout'),
    path('search/', search, name='search'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
