from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    details = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.title}'


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} by {self.item.title}'

    def get_total_price(self):
        return (self.quantity) * (self.item.price)
    #
    # def get_total_discount_price(self):
    #     return (self.quantity) * (self.item.discount_price)
    #
    # def total_amount_saving(self):
    #     return (self.get_total_price())-(self.get_Total_discount_price())
    #
    # def get_final_price(self):
    #     if self.item.discount_price:
    #         return self.get_total_discount_price()
    #     return self.get_total_price()


class Address(models.Model):
    st_address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(verbose_name='Zip', max_length=6)

    class Meta:
        verbose_name_plural='Address'

    def __str__(self):
        return f'{self.st_address} of {self.city}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user.username}'

    def final_order_price(self):
        total = 0
        for orderitem in self.items.all():
            total += (orderitem.quantity) * (orderitem.item.price)
        return total
