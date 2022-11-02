from django.shortcuts import render, get_object_or_404, redirect
from .forms import CreateUser, AddressForm
from django.contrib.auth import login, authenticate
from .models import OrderItem, Order, Item
from django.views.generic.list import ListView
from django.db.models import F, Q
from django.utils import timezone
from django.contrib import messages
from django.views.generic import View, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def register(request):
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home', permanent=True)

    else:
        form = CreateUser()
    return render(request, 'store/register.html', {'form': form})


def home(request):
    return render(request, 'store/home-page.html')


class Home(ListView):
    model = Item
    template_name = 'store/Home.html'


@login_required
def add_to_cart(request, id):
    item = get_object_or_404(Item, pk=id)
    orderitem, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            orderitem.quantity = F('quantity') + 1
            orderitem.save()
        else:
            order.items.add(orderitem)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered=False, ordered_date=ordered_date)
        order.items.add(orderitem)
    return redirect('home')


@login_required
def add_single_to_cart(request, id):
    item = get_object_or_404(Item, pk=id)
    orderitem, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            orderitem.quantity = F('quantity') + 1
            orderitem.save()
        else:
            order.items.add(orderitem)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date, ordered=False)
        order.add(orderitem)
    return redirect('order-summary')


@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(Item, pk=id)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            orderitem = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            orderitem.quantity = 1
            orderitem.save()
            order.items.remove(orderitem)
            messages.success(request, f'{orderitem} removes successfully.')
        else:
            messages.info(request, 'No Such Product exist in Your order.')
            return redirect('home')
    else:
        messages.info(request, f"You don't have any pending order.")
        return redirect('home')
    return redirect('home')


@login_required
def remove_single_item_from_cart(request, id):
    item = get_object_or_404(Item, pk=id)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            orderitem = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if orderitem.quantity > 1:
                orderitem.quantity -= 1
                orderitem.save()
            else:
                orderitem.quantity = 1
                orderitem.save()
                order.items.remove(orderitem)
                messages.success(request, f'{orderitem} removes successfully.')
        else:
            messages.info(request, 'No Such Product exist in Your order.')
            return redirect('order-summary')
    else:
        messages.info(request, f"You don't have any pending order.")
        return redirect('order-summary')
    return redirect('order-summary')


class Order_Summary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order_qs = Order.objects.filter(user=self.request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            return render(self.request, 'store/ordersummary.html', {'order': order or None})
        return render(self.request, 'store/ordersummary.html', )


class Checkout(View):
    def get(self, *args, **kwargs):
        # order = None
        form = AddressForm()
        order_qs = Order.objects.filter(user=self.request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
        return render(self.request, 'store/checkout-page.html', {'order': order or None, 'form': form})

    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            form = AddressForm(self.request.POST)
            if form.is_valid():
                form.save()
                st_address = form.cleaned_data.get('st_address')
                city = form.cleaned_data.get('city')
                order_qs = Order.objects.filter(user=self.request.user, ordered=False)
                if order_qs.exists():
                    order = order_qs[0]
                    order.ordered = True
                    order.save()
                messages.success(self.request,
                                 f"Your order is placed with name {self.request.user}  and with address {city} {st_address}")
                return redirect('home')
        return render(self.request, 'store/checkout-page.html', {'form': form})


def search(request):
    query = request.GET.get('query', '')
    if query.isdigit():
        query = int(query)
        result = Item.objects.filter(Q(price__lte=query))

        return render(request, 'store/search.html', {'result': result})
    print(type(query))
    if query:
        result = Item.objects.filter(Q(title__icontains=query) | Q(details__icontains=query))

        return render(request, 'store/search.html', {'result': result})
    else:
        return redirect('home')
