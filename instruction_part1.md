# Установка проекта

Создадим у себя на диске папку для проекта. В этой папке создадим папку media, в ней будут сохраняться картинки товаров.
Откройте командную строку и перейдите в папку проекта
В папке проекта создайте виртуальное окружение

## Создание виртуального окружения

```
python -m venv env
```

входим в виртуальное окружение

- для windows
  env\Scripts\activate
- для Linux:
  source env/bin/activate

обновим установщик

```
python -m pip install --upgrade pip
```

в окружение установим Django

```
pip install django
```

или через файл requirements.txt
в него добавим одну строку:
django

в этом случае установка

```
pip install -r requirements.txt
```

создаем проект django

```
django-admin startproject sushi_delivery_shop
```

для удобства переименуем папку c django проектом в app

```
mv sushi_delivery_shop app
```

перейдем в папку проекта и запустим сервер для разработки

```
cd app
python manage.py runserver
```

Сервер будет доступен по адресу http://127.0.0.1:8000/
Скрипт сообщает о том что есть не применённые миграции, применим их. Для этого остановим сервер cttl+c и выполним команду

```
python manage.py migrate
```

теперь создадим суперпользователя для админки

```
python manage.py createsuperuser
```

Запустим сервер командой runserver и зайдем в админку под новым пользователем по адресу http://127.0.0.1:8000/

В папке app разместим папку static (приложена к уроку)


Отредактируем settings.py и добавим туда следующее

sushi_delivery_shop/settings.py

```
import os

LANGUAGE_CODE = 'ru'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, '../static')
MEDIA_ROOT = os.path.join(BASE_DIR, '../media')
```

Добавим пути для отображения статических файлов (js, css, итд) в urls.py

sushi_delivery_shop/urls.py

```
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

После этого можно проверить правильно ли все настроено
http://127.0.0.1:8000/static/css/roboto.css
по этому адресу должен показаться файл со стилями для шрифта

Создадим приложение shop

```
python manage.py startapp shop
```

добавим новое приложение в settings.py - добавим приложение shop  в INSTALLED_APPS

```
INSTALLED_APPS = [
    ...
    'shop',
]
```

создадим urls.py в shop и добавим туда путь до главной страницы нашего приложения

```
from django.urls import path, include
from shop.views import  index

urlpatterns = [
    path('', index, name='index'),
]
```

и в главном urls.py  добавим пути приложения shop

```
path('', include('shop.urls')),
```

во views.py добавим представление для главной страницы

```
from django.shortcuts import render

def index(request):
    context = {
        'title': 'Главная страница',
    }
    return render(request, 'index.html', context)
```

создадим в папке shop папку templates а в ней шаблоны index.html и base.html

base.html

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}СушиShop{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock content %}
</body>
</html>
```

index.html

```
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <p>Hello</p>
    <a href="/products/">Перейти в каталог</a>
{% endblock %}
```

На главной можем увидеть результат http://127.0.0.1:8000/

Теперь добавим модель для Товара в файле models.py

```
class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.name
```

для работы с картинками нужна библиотека pillow. Установим ее.

```
pip install pillow
```

После создания модели необходимо создать миграции и применить их для обновления базы данных

```
python manage.py makemigrations
python manage.py migrate
```

Выведем товары в админку. для этого отредактируем admin.py приложения shop

shop/admin.py

```
from django.contrib import admin
from shop.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ['id', 'name', 'price', 'image']
    list_editable = ['name', 'price', 'image']
```

Сами товары создадим в админке руками или добавим из дампа базы данных shop.json

```
python manage.py loaddata shop.json
```

Теперь выведем  товары на сайте с помощью class based generic view. Нам нужен список товаров и страница товара.

shop/urls.py

```
from django.urls import path, include
from shop.views import ProductListView, ProductDetailView, index

urlpatterns = [
    path('', index, name='index'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
```

shop/views.py

```
# Импорт функции render для отображения HTML-страниц
from django.shortcuts import render

# Импорт классов ListView и DetailView для создания представлений на основе классов
from django.views.generic import ListView, DetailView

# Импорт модели Product из приложения shop
from shop.models import Product

# Определение функции представления для главной страницы
def index(request):
    # Словарь с данными, которые будут переданы в шаблон
    context = {
        'title': 'Доставка суши SusiShop',  # Заголовок страницы
    }
    # Возврат сгенерированной HTML-страницы с переданными данными
    return render(request, 'index.html', context)

# Определение класса представления для отображения списка продуктов
class ProductListView(ListView):
    # Указание модели, с которой будет работать представление
    model = Product
    # Шаблон для отображения списка продуктов
    template_name = 'product_list.html'
    # Имя переменной контекста для списка продуктов в шаблоне
    context_object_name = 'products'

    # Переопределение метода для фильтрации и сортировки списка продуктов
    def get_queryset(self):
        # Получение базового набора объектов
        queryset = super().get_queryset()
        # Получение значения параметра сортировки из запроса
        sort_option = self.request.GET.get('sort')
        # Сортировка по возрастанию, если sort_option = 'asc'
        if sort_option == 'asc':
            queryset = queryset.order_by('name')
        # Сортировка по убыванию, если sort_option = 'desc'
        elif sort_option == 'desc':
            queryset = queryset.order_by('-name')
        # Возвращение отсортированного набора объектов
        return queryset

# Определение класса представления для отображения детальной информации о продукте
class ProductDetailView(DetailView):
    # Указание модели, с которой работает представление
    model = Product
    # Шаблон для отображения информации о продукте
    template_name = 'product_detail.html'
    # Имя переменной контекста для продукта в шаблоне
    context_object_name = 'product'
```

shop/templates/product_list.html

```
{% extends  'base.html' %}

{% block content %}
    <div>
        {% for product in products %}
        <div>
            <a href="{% url 'product_detail' pk=product.pk %}">
                <h2>{{ product.name }}</h2>
            </a>
          
            <div>
                {% if product.image %}
                    <img src="{{product.image.url}}">
                {% endif %}
            </div>

            <div>Цена: {{ product.price|floatformat:0 }} ₽</div>
        </div>
        {% endfor %}
    </div>
{% endblock content %}
```

shop/tempaltes/product_detail.html

```
{% extends  'base.html' %}

{% block content %}
    <div>
        <div>
            {% if product.image %}
                <img src="{{ product.image.url }}" alt="{{ product.name }}">
            {% endif %}
        </div>
        <h2>{{ product.name }}</h2>
        <div>{{ product.description }}</div>
        <div>Цена: {{ product.price|floatformat:0 }} ₽</div>
    </div>
{% endblock content %}
```
