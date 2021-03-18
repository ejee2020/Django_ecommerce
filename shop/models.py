from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class Filter(models.Model):
    Color = models.CharField(max_length=200, db_index=True)
    Price_range = models.CharField(max_length=200, db_index=True)
    Size = models.CharField(max_length=200, db_index=True)
    Brand = models.CharField(max_length=200, db_index=True)

    class Meta:
        ordering = ['Color']

    def __str__(self):
        return self.Color


class Sorted(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    meta_description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, allow_unicode=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:sort_in_slug', args=[self.slug])


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    meta_description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, allow_unicode=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_in_category', args=[self.slug])


SIZE_CHOICES = (
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("One Size", "One Size"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
)

COLOR_CHOICES = (
    ("Black", "Black"),
    ("Blue", "Blue"),
    ("Brown", "Brown"),
    ("Burgundy", "Burgundy"),
    ("Camel", "Camel"),
    ("Green", "Green"),
    ("Grey", "Grey"),
    ("Navy", "Navy"),
    ("Orange", "Orange"),
    ("Pink", "Pink"),
    ("Purple", "Purple"),
    ("Red", "Red"),
    ("White", "White"),
    ("Yellow", "Yellow"),
)

STAR_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
)

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='products')
    brand = models.CharField(max_length=50, default="")
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    size_and_fits = models.TextField(blank=True)
    details = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    size = models.CharField(default='S', max_length=20, choices=SIZE_CHOICES)
    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    view = models.PositiveIntegerField(default=0)
    color = models.CharField(default='', max_length=20, choices=COLOR_CHOICES)

    class Meta:
        ordering = ['-created', '-updated']
        index_together = [['id', 'slug']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        self.view += 1
        self.save()
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def put_into_wishlist(self):
        return reverse('shop:put_into_wishlist', args=[self.id])

    def remove_from_wishlist(self):
        return reverse('shop:remove_from_wishlist', args=[self.id])


class Review(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    stars = models.CharField(default='0', max_length=20, choices=STAR_CHOICES)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_in_category', args=[self.title])


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True)
    items = models.ManyToManyField(Product)

    def __str__(self):
        return self.user


class Support(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    query = models.TextField(max_length=400)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.last_name


class SupportList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True)
    supports = models.ManyToManyField(Support)

    def __str__(self):
        return self.user


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    created = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        default='Male', max_length=20, choices=GENDER_CHOICES)
