# Урок 2 по созданию WEB-приложений

1.	Создание корзины.
2.	Создание стилей интерфейса.

# Запуск проекта

1.	Откроем в VSCode проект с предыдущего урока (корневая папка webapp)
2.	Создадим (если ещё не создано) и войдем в виртуальное окружение,
установим библиотеки:
```
python -m venv .venv 
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

```

3.	Запустим сервер
```
cd app
python manage.py runserver
```
(база данных уже есть в проекте. Доступ к админке admin:admin)

4.	Откройте сайт в браузуре:
```
http://127.0.0.1:8000
```

5.	Скачайте в другую папку материалы из текущего урока
(некоторые файлы будем брать из этих материалов)

# Подключение стилей и шрифта

1.	Скопируйте из материалов текущего урока файл базового шаблона
app\shop\templates\base.html в одноименную папку проекта:
app\shop\templates\

2.	Скопируйте из материалов текущего урока файл
app\static\css\style.css в одноименную папку проекта:
app\static\css\

3.	В файле shop\templates\base.html подключите стили
в любом месте блока "head":
```html
<head>
    ...
    <link rel="stylesheet" type="text/css" href="/static/css/style.css">
    <link href="/static/css/roboto.css" rel="stylesheet">
	...
</head>
```

# Изменение шаблона каталога товаров

1.	Скопируйте из материалов текущего урока файл
app\shop\templates\product_list.html в одноименную папку проекта:
app\shop\templates\

2.	Скопируйте из материалов текущего урока файл
app\shop\views.py в одноименную папку проекта:
app\shop\

3.	Откройте в браузере страницу с каталогом товаров:
```
http://127.0.0.1:8000/products/
```

# Изменение шаблона страницы товара

1.	Скопируйте из материалов текущего урока файл
app\shop\templates\product_detail.html в одноименную папку проекта:
app\shop\templates\

2.	Скопируйте из материалов текущего урока файл
app\static\css\detail.css в одноименную папку проекта:
app\static\css\

3.	Откройте в браузере страницу с товаром, например id=9:
```
http://127.0.0.1:8000/products/9/
```

# Изменение шаблона главной страницы

1.	Скопируйте из материалов текущего урока файл
app\shop\templates\index.html в одноименную папку проекта:
app\shop\templates\

2.	Обращаемся в ChatGPT с таким запросом:
```
Напиши тексты главной страницы для сервиса доставки СушиShop.
Текст должен быть информативным, привлекательным и убедительным,
привлекая внимание потенциальных клиентов и мотивируя их сделать заказ.
Для разметки используй теги h2,p, ul, li. Можешь использовать emodji 
```

3.	Полученный текст вставим в шаблон app\show\templates\index.html
в блок content__container:
```
<div class="content__container">
    ...
</div>
```

# Выведем товары по акции на главной странице

1.	Добавим поле "товар по акции" для товара

Определите новое поле "товар по акции" в модели Product
в файле app\shop\models:
```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    on_sale = models.BooleanField(default=False)  # Новое поле "товар по акции"

    def __str__(self):
        return self.name
```

2.	Создайте и примените миграцию для обновления базы данных с новым полем. В терминале выполните следующие команды:
```
python manage.py makemigrations
python manage.py migrate
```

3.	Посмотрите - как выглядит добавленное поле в базе данных,
предварительно установив расширение "SQLite Viewer".
Затем вы можете посмотреть базу данных app\db.sqlite3
выполнив двойной щелчок над этим файлом.

4.	Также можно вывести поле on_sale для удобного редактирования
прямо в списке товаров в админке app\shop\admin.py:
```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ['id', 'name', 'price', 'on_sale']
    list_editable = ['name', 'price', 'on_sale',]
```

5.	Теперь вы можете использовать новое поле on_sale в ваших запросах к модели Product.
Например, чтобы получить все товары по акции, вы можете использовать фильтр
в файле app\shop\views.py:
```python
def index(request):
    context = {
        'title': 'Доставка суши SusiShop',
        'products_on_sale': Product.objects.filter(on_sale=True)
    }
    return render(request, 'index.html', context)
```

6.	После этого можно вывести товары по скидке на главной странице,
добавив вывод товаров в шаблон app\shop\templates\index.html:
```html
{% if products_on_sale %}
    <h2>💰 Скидки 🎉</h2>
    <p>Не упустите шанс сэкономить на вашем заказе! Используйте наши акции и специальные предложения, чтобы насладиться вкусными суши по выгодной цене.</p>
    <div class="popular-product__container">
        {% for product in products_on_sale %}
            <a class="popular-product__item__header popular-product__item" href="{% url 'product_detail' pk=product.pk %}">
                <h4>{{ product.name }}</h4>
                <div class="popular-product__item__photo__container">
                    {% if product.image %}
                        <img class="popular-product__item__photo" src="{{product.image.url}}">
                    {% endif %}
                </div>
                <div class="popular-product__item__price">Цена: {{ product.price|floatformat:0 }} ₽</div>
            </a>
        {% endfor %}
    </div>
{% endif %}
```

# Работа в shell с объектами моделей

1.	Запуск Django shell:
```
python manage.py shell
```

2.	Импорт модели Product:
```python
from shop.models import Product
```

3.	Создание нового объекта Product и сохраните его в базе данных:
```python
new_product = Product(name='Сет №1', description='Лучший сет', price=3333)
new_product.save()
```

4.	Обновление атрибута image у объекта new_product:
```python
new_product.image = 'products/Императорский_сашими.png'
new_product.save()
```

5.	Получение всех объектов модели Product:
```python
all_products = Product.objects.all()
for product in all_products:
    print(product.name, product.price)
```

6.	Получение конкретного объекта Product и вывод его атрибутов:
```python
specific_product = Product.objects.get(name='Симфония океана')
print(specific_product.description)
```

7.	Получение Product у которого цена ниже 2000
```python
products_under_2000 = Product.objects.filter(price__lt=2000)
for product in products_under_2000:
    print(product.name, product.price)
```

8.	Получить список значений атрибута
```
price_values = all_products.values_list('price', flat=True)
print(price_values)
```

9.	Получить список значений атрибута, у которых цена больше 3000
```
price_values = price_values.filter(price__gt=3000)
print(price_values)
```

10.	Получить список значений атрибута, у которых цена больше 3000,
отсортированных по возрастанию
```
price_values = price_values.order_by('price')
print(price_values)
```

11. Удаление объекта new_product:
```python
new_product.delete()
```

12.	Получение первого объекта из QuerySet
```
first_product = Product.objects.first()
print(first_product.name, first_product.price)
```

13.	Получение последнего объекта из QuerySet
```
last_product = Product.objects.last()
print(last_product.name, last_product.price)
```

14.	Фильтрация объектов по нескольким условиям (логическое "И"):
```
filtered_products = Product.objects.filter(price__gt=2000, price__lt=5000)
for product in filtered_products:
    print(product.name, product.price)
```

15.	Фильтрация объектов по логическому "ИЛИ":
```
from django.db.models import Q
products_or_condition = Product.objects.filter(Q(price__lt=2000) | Q(name__icontains='Сашими'))
for product in products_or_condition:
    print(product.name, product.price)
```

16.	Агрегация данных (максимальная цена):
```
from django.db.models import Max
max_price = Product.objects.aggregate(Max('price'))
print(max_price['price__max'])
```

17.	Подсчёт количества объектов:
```
product_count = Product.objects.count()
print(f"Всего продуктов: {product_count}")
```

18.	Выборка уникальных значений из поля:
```
unique_prices = Product.objects.values_list('price', flat=True).distinct()
print(unique_prices)
```

19.	Получение случайного объекта:
```
from random import choice
random_product = choice(Product.objects.all())
print(random_product.name)
```

20.	Обновление нескольких объектов сразу:
```
Product.objects.filter(price__lt=2000).update(description='Скидка на продукт')
```

21.	Проверка существования объектов по условию
```python
exists = Product.objects.filter(name='Симфония океана').exists()
print("Существует" if exists else "Не существует")
```

22.	Получение QuerySet в виде словаря
```python
products_dict = Product.objects.values('id', 'name', 'price')
print(list(products_dict))
```

23.	Удаление всех объектов из модели
```python
Product.objects.all().delete()
```

24.	Получение объектов с аннотацией (пример с количеством продуктов)
```python
from django.db.models import Count
category_products = Product.objects.values('category').annotate(product_count=Count('id'))
print(category_products)
```

25.	Ограничение количества возвращаемых объектов
```python
limited_products = Product.objects.all()[:5]
for product in limited_products:
    print(product.name)
```

26.	Сортировка объектов по нескольким полям
```python
sorted_products = Product.objects.order_by('price', '-name')
for product in sorted_products:
    print(product.name, product.price)
```

27.	Создание объекта с помощью create()
```python
new_product = Product.objects.create(name='Сет №2', description='Второй сет', price=4500)
```

28.	Копирование объекта
```python
original_product = Product.objects.get(name='Сет №1')
copied_product = Product.objects.create(
    name=f"{original_product.name} (Копия)",
    description=original_product.description,
    price=original_product.price
)
```

29.	Получение объектов с исключением определённого условия
```python
not_in_condition = Product.objects.exclude(price__lt=2000)
for product in not_in_condition:
    print(product.name, product.price)
```

30.	Увеличение значения поля для всех объектов
```python
from django.db.models import F
Product.objects.update(price=F('price') + 100)
```

31. Использование транзакций для атомарных операций
```python
from django.db import transaction
with transaction.atomic():
    Product.objects.create(name='Сет №3', price=5000)
    Product.objects.create(name='Сет №4', price=6000)
```

# Расширение для просмотра базы SQLite3

Название расширения "Viewer SQLite". В бесплатной версии работает только 
в режиме просмотра данных

# Добавление на сайт Корзины 

1.	Скопируйте из материалов текущего урока папку
app\cart в одноименную папку проекта app\

2.	Добавим приложение cart в INSTALLED_APPS
sushi_delivery_shop/settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'cart', 
]
```

3.	Создадим и применим миграции
```
python manage.py makemigrations
python manage.py migrate
```

4.	Добавим пути приложения cart в основной файл
api\sushi_delivery_shop\urls.py
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cart.urls')),
    path('', include('shop.urls')),
]
```

5.	Добавим кнопку добавления товара в корзину в карточки каталога
shop\templates\product_list.html
```html
<div class="catalog__item">
    ...
    
    {% include 'includes/buy_button.html' %}
</div>
```

6.	Добавим кнопку добавления товара в корзину на страницу товара
shop\templates\product_detail.html
```html
<div class="product-detail__info">
    ...
    {% include 'includes/buy_button.html' %}
</div>
```

# Расширение для автодополнения кода (для самостоятельного изучения)

Название расширения: Codeium
(требует регистрации)

# Домашние задания (для самостоятельного изучения)

## ДЗ Lite

Повторить урок

## ДЗ Pro

Добавить поле "Популярные товары"