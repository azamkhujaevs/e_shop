from django.db import models


#    Таблица категории.
class Category(models.Model):
    categoryy_name = models.CharField(max_length=15)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categoryy_name


#    Таблица для продуктов
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_count = models.IntegerField()
    product_des = models.TextField()
    product_photo = models.ImageField(upload_to='media')
    product_price = models.FloatField()
    product_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.product_name


#    Таблица корзины для пользователей
class Usercart(models.Model):
    user_id = models.IntegerField()
    user_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_for_product = models.FloatField()


#  Таблица для акций
class Sale(models.Model):
    sale_name = models.CharField(max_length=120)
    sale_products = models.ManyToManyField(Product)
    sale_start = models.DateField()
    sale_end_date = models.DateField()

    def __str__(self):
        return self.sale_name


#    Таблица для обратной связи
class Feedback(models.Model):
    user_id = models.IntegerField()
    feed_text = models.TextField()
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.feed_text
