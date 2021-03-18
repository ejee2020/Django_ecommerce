from django.db.models.signals import post_save
import hashlib
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from coupon.models import Coupon
from shop.models import Product
from django.contrib.auth.models import User
