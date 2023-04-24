from django.shortcuts import render, redirect
from . import models

from telebot import TeleBot

bot = TeleBot('5986372537:AAFDD5AQHdf92vds_0dui_-ejeJkK2R2ef8', parse_mode='HTML')


# Create your views here.
def home(request):
    # Получить продукты из базы
    all_products = models.Product.objects.all()

    # Получить все названия категорий
    all_categories = models.Category.objects.all()  # SELECT * FROM category

    # Передать на front часть
    context = {'products': all_products, 'categories': all_categories}

    return render(request, 'index.html', context)


# Функция для отображения информаций о конкретном продукте
def about_product(request, pk):
    # Получить конкретный продукт или данные из базы
    current_product = models.Product.objects.get(product_name=pk)

    context = {'product': current_product}

    return render(request, 'about.html', context)


# Продукты из конкретной категории
def category_products(request, pk):
    category = models.Category.objects.get(categoryy_name=pk)
    products_from_category = models.Product.objects.filter(product_category=category)

    context = {'products': products_from_category}

    return render(request, 'index.html', context)


# Поиск товаров
def search_for_product(request):
    product_from_front = request.GET.get('search')
    find_product_from_db = models.Product.objects.filter(product_name__contains=product_from_front)

    context = {'products': find_product_from_db}

    return render(request, 'index.html', context)


# Добавить продукт в корзину
def add_product_to_cart(request, pk):
    # Получаем сам продукт
    current_product = models.Product.objects.get(id=pk)

    # Добавим в корзину
    checker = models.Usercart.objects.filter(user_id=request.user.id, user_product=current_product)

    # Проверка
    if checker:
        # Если продукт уде добавлен, то изменим количество
        checker[0].quantity = int(request.POST.get('pr_count'))
        checker[0].total_for_product = current_product.product_price * checker[0].quantity

    else:
        # Если нет продукта в корзине, то добавим
        models.Usercart.objects.create(user_id=request.user.id,
                                       user_product=current_product,
                                       quantity=request.POST.get('pr_count'),
                                       total_for_product=current_product.product_price * int(
                                           request.POST.get('pr_count')))

    return redirect(f'/product-detail/{current_product.product_name}')


# Страница корзины пользователя
def get_user_cart(request):
    user_cart = models.Usercart.objects.filter(user_id=request.user.id)

    context = {'user_cart': user_cart}

    return render(request, 'cart.html', context)


# Удаление товара из корзины
def delete_pr_from_cart(request, pk):
    prod_to_delete = models.Usercart.objects.get(id=pk)

    prod_to_delete.delete()

    return redirect('/cart')


# Оформление заказа и отправка в тг
def order_zakaz(request):
    # Получить корзину пользователя
    user_cart = models.Usercart.objects.filter(user_id=request.user.id)

    # Получить введенные данные (имя, номер телефона, адрес)
    username = request.POST.get('username')
    phone_number = request.POST.get('phone_number')
    address = request.POST.get('address')

    # Посчитать итог
    result = sum([i.total_for_product for i in user_cart])

    # Формируем сообщение для тг(инвойс)
    invoice_message = f'<b>Новый заказ</b>\n\n<b>Имя:</b> {username}\n<b>Номер:</b> {phone_number}\n<b>Адрес доставки:</b> {address}\n-------\n'

    for i in user_cart:
        invoice_message += f'<b>{i.user_product}</b> X <b>{i.quantity}</b> = <b>{i.total_for_product}</b>\n'

    invoice_message += f'\n-----------\n<b>Итог:</b> {result} сум'

    # Отправим сообщение в бот, где есть админ
    bot.send_message(638384527, invoice_message)

    return redirect('/')
