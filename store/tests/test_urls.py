from django.test import SimpleTestCase
from django.urls import reverse, resolve
from store.views import (
    register, home, Home,
    add_to_cart, remove_from_cart,
    Order_Summary, remove_single_item_from_cart,
    add_single_to_cart, Checkout, search,
)


class TestURLS(SimpleTestCase):
    def test_home_view(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, Home)

    def test_register_view(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_add_to_cart_view(self):
        url = reverse('add-to-cart', args=[id])
        self.assertEquals(resolve(url).func, add_to_cart)

    def test_add_signle_to_cart_view(self):
        url = reverse('add-single-to-cart', args=[id])
        self.assertEquals(resolve(url).func, add_single_to_cart)

    def test_remove_from_cart_view(self):
        url = reverse('remove-from-cart', args=[id])
        self.assertEquals(resolve(url).func, remove_from_cart)

    def test_remove_single_from_cart_view(self):
        url = reverse('remove-single-item', args=[id])
        self.assertEquals(resolve(url).func, remove_single_item_from_cart)

    def test_checkout_view(self):
        url = reverse('checkout')
        self.assertEquals(resolve(url).func.view_class, Checkout)

    def test_order_summary_view(self):
        url = reverse('order-summary')
        self.assertEquals(resolve(url).func.view_class, Order_Summary)

    def test_search_view(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, search)
