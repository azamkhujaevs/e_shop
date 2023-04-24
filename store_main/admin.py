from django.contrib import admin
from .models import Product,Category,Feedback,Usercart,Sale
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Feedback)
admin.site.register(Usercart)
admin.site.register(Sale)