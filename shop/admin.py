from django.contrib import admin
from .models import *
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)
                           }


admin.site.register(Category, CategoryAdmin)


@admin.register(Product)  # annotation
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'category', 'price', 'stock',
                    'available_display', 'available_order', 'created', 'updated', 'view']
    list_filter = ['available_display', 'available_order',
                   'created', 'updated', 'category']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'available_display', 'available_order']


class SortAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)
                           }


admin.site.register(Sorted, SortAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'stars', 'product', 'created', 'updated']


admin.site.register(Review, ReviewAdmin)


class WishListAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(WishList, WishListAdmin)


class SupportAdmin(admin.ModelAdmin):
    list_display = ['first_name']


admin.site.register(Support, SupportAdmin)
