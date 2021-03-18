from django.db.models.signals import post_save
import hashlib
from .iamport import payments_prepare, find_transaction
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
from coupon.models import Coupon
from shop.models import Product, User


class Order(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT,
                               related_name='order_coupon', null=True, blank=True)
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10000)])

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Order {self.id}'

    def get_total_product(self):
        return sum(item.get_item_price() for item in self.items.all())

    def get_total_price(self):
        total_product = self.get_total_product()
        return total_product - self.discount


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='order_products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_item_price(self):
        return self.price * self.quantity


class OrderTransactionManager(models.Manager):
    def create_new(self, order, amount, success=None, transaction_status=None):
        if not order:
            raise ValueError("주문 정보 오류")

        transaction = self.model(
            order=order,
            amount=amount
        )

        try:
            transaction.save()
        except Exception as e:
            print("save error", e)

        return transaction.id

    def get_transaction(self, merchant_order_id):
        result = find_transaction(merchant_order_id)
        if result['status'] == 'paid':
            return result
        else:
            return None


class OrderTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    merchant_order_id = models.CharField(max_length=12, null=True, blank=True)
    transaction_id = models.CharField(max_length=120, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_status = models.CharField(
        max_length=220, null=True, blank=True)
    type = models.CharField(max_length=120, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    objects = OrderTransactionManager()

    def __str__(self):
        return str(self.order.id)

    class Meta:
        ordering = ['-created']


def order_payment_validation(sender, instance, created, *args, **kwargs):
    if instance.transaction_id:
        iamport_transaction = OrderTransaction.objects.get_transaction(
            merchant_order_id=instance.merchant_order_id)
        merchant_order_id = iamport_transaction['merchant_order_id']
        imp_id = iamport_transaction['imp_id']
        amount = iamport_transaction['amount']
        local_transaction = OrderTransaction.objects.filter(merchant_order_id=merchant_order_id,
                                                            transaction_id=imp_id, amount=amount).exists()

        if not iamport_transaction or not local_transaction:
            raise ValueError("invalid transaction")


# after orderTransaction gets saved, run order-paymnet_alidation
post_save.connect(order_payment_validation, sender=OrderTransaction)
