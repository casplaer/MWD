from django.contrib import admin

# Register your models here.

from .models import FAQ, Cart, CartItem, Coupon, New, Order, Product, Job, Review, Contact, Profile, Partner, AboutUs

admin.site.register(Product)
admin.site.register(Job)
admin.site.register(Review)
admin.site.register(Coupon)
admin.site.register(Contact)
admin.site.register(New)
admin.site.register(FAQ)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Partner)
admin.site.register(AboutUs)