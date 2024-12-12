# Урок 3 по созданию WEB-приложений

На этом уроке:

1. Добавим нейроконсультанта на наш сайт.
2. Сгенерируем базу знаний, на основе которой будет отвечать наш сайт.
3. Возможность из чата положить товар в корзину.
4. Сделаем корзину без перезагрузки страницы.

# Запуск проекта

1. Откроем в VSCode проект с предыдущего урока (корневая папка webapp)
2. Создадим (если ещё не создано) и войдем в виртуальное окружение,
   установим библиотеки:

```
python -m venv env 
env\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

```

3. Запустим сервер

```
cd app
python manage.py runserver
```

4. Откройте сайт в браузуре:

```
http://127.0.0.1:8000
```

5. Попробуйте открыть админку http://127.0.0.1:8000/admin и, если не открывается, то закомментируйте строку в файле shop/sushi_delivery_shop/urls.pr:

```
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Зайдите в админку, затем раскомментируйте ту же строку
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

6. Скачайте в другую папку материалы из текущего урока
   (некоторые файлы будем брать из этих материалов)

# Создание кнопки AJAX для добавления в корзину

1. Скопируйте из материалов урока в
   каталог app\cart\templates\includes файлы шаблонов кнопки и всплывающего сообщения:

```
ajax_buy_button.html
add_to_cart_popup.html
```

2. Добавим папку с иконкой корзины в папку app\static:

```
icons\cart.svg
```

3. Добавим в шаблон app\shop\templates\base.html и высплывающее сообщение:

```html
<nav class="navbar">
    <a class="header__logo" href="{% url 'index' %}">СушиShop</a>
    <a class="cart-link" href="{% url 'cart' %}">
        <img class="cart-link__icon" src="/static/icons/cart.svg" width="30" height="30" alt="Корзина">
        {% include 'includes/add_to_cart_popup.html' %}
    </a>
</nav>
```

4. В файле шаблона app\shop\templates\product_detail.html добавим кнопку в конце блока '.product-detail__info':

```
<div class="product-detail__info">
    ...
    {% include 'includes/ajax_buy_button.html' %}
</div>
```

Если присутствует старая кнопка корзины, её необходимо удалить:

```
{% include 'includes/buy_button.html' %}
```

5. В файле шаблона app\shop\templates\product_list.html добавьте кноппку в конец блока '.catalog__item':

```
<div class="catalog__item">
    ...
    {% include 'includes/ajax_buy_button.html' %}
</div>
```

Если присутствует старая кнопка корзины, её необходимо удалить:

```
{% include 'includes/buy_button.html' %}
```

# Добавляем виджет консультанта на все страницы

1. Скопируйте из материалов урока в
   каталог app\ каталог приложения:

```
app\neuro_assistant
```

2. С помощью другого терминала примените миграции (не забудьте войти в виртуальное окружиние и перейти в каталог app в терминале):

```
python manage.py migrate
```

3. Добавьте приложение neuro_assistant в файл app\sushi_delivery_shop\settings.py в список INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...
    'neuro_assistant',
]
```

4. Добавьте пути приложения в app\sushi_delivery_shop\urls.py:

```python
urlpatterns = [
    ...
    path('neuro_assistant/', include('neuro_assistant.urls')),
]
```

С помощью другого терминала примените миграции (не забудьте войти в виртуальное окружиние и перейти в каталог app в терминале):

```
python manage.py migrate
```

6. После этого диалог будет доступен по адресу http://127.0.0.1:8000/neuro_assistant/dialog/
7. Добавим виджет консультанта в главнй шаблон
   app\shop\templates\base.html:

```html
<body>
    ...

    {% include 'includes/dialog_widget.html' %}
</body>
```

7. Виджет устроен так, что в окне диалога показывается iframe который показывает другую страницу.Чтобы разрешить такой режим, нужно добавить настройку в app\sushi_delivery_shop\settings.py:

```python
X_FRAME_OPTIONS = 'SAMEORIGIN'
```

# База знаний

1. Наш консультант будет работать на базе знаний созданной из каталога, но также для него нужна информация о доставке и другая информация которую периодически нужно будет обновлять.
   Для этих целей созданы модели Category и Chunk в models.py нейроассистанта и выведены в админке. Теперь можо перейти в админку и заполнить чанки для базы знаний.
2. Обратимся к GPT для создания базы знаний компании.

"Мы составляем базу знаний о компании "СушиShop", занимающейся доставкой суши и роллов. База знаний должна покрывать  ответами все вероятные вопросы пользователя.
база знаний состоит из чанков, каждый чанк имеет категорию.
Перечислите все категории"

```
1. Меню
2. Доставка
3. Оплата
4. Акции и скидки
5. Качество продукции
6. Работа сотрудников
7. Режим работы
8. Контактная информация
9. Информация о компании
```

Далее запросим чанки для необходимых категорий
"Напишите пример для категории "Доставка"

```
Мы осуществляем бесплатную доставку суши и роллов в пределах города при заказе на сумму от 1000 рублей. Время доставки составляет примерно 30-40 минут, в зависимости от загруженности дорог и количества заказов. Для уточнения деталей по доставке в вашем районе, пожалуйста, свяжитесь с нашим оператором по телефону или посетите раздел "Доставка" на нашем сайте.
```

3. Далее можем попросить его написать чанки для каждой категории и сами категории в формате json:

"""
Мы составляем базу знаний о компании "СушиShop", занимающейся доставкой суши и роллов. База знаний должна покрывать  ответами все вероятные вопросы пользователя.
база знаний состоит из чанков, каждый чанк имеет категорию. Перечислите все категории

Сгененируй демо-данные чанков для каждой категории и создай текст формата json для возможности импорта категорий и чанков в базу данных sqlite3 , чтобы можно было всю информацию импортировать средствами python manage.py фреймворка Django

Имя приложения neuro_assistant, описание модели:
class Category(models.Model):
    name = models.CharField(max_length=255)
class Chunk(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField()
"""

4. Импортируем чанки и категории в базу данных.

```
python manage.py loaddata chunks.json
```

5. Для того чтобы консультант имел возможность показывать ссылки на товары добавим метод для модели товара в приложении shop.
   Воспользуемся функцией reverse которая вернет адрес для данной модели по названию указанному в urls.py
   app\shop\models.py

```python
from django.urls import reverse
class Product(models.Model):
    ... 
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.pk)])
```

# WEB-сервис на базе FastAPI

1. Скопируйте из материалов урока в
   корневой каталог webapp каталог с WEB-сервисом FastAPI.
2. Экспортируем из базы данных sqlite3 базу знаний с помощью команды, которую напишем в Django в файле app\neuro_assistant\management\commands\chunks_export.py

```
from django.core.management.base import BaseCommand
from neuro_assistant.models import Category, Chunk
from shop.models import Product

class Command(BaseCommand):
    help = 'Export all chunks to a text file'

    def handle(self, *args, **options):
        relative_path = '../api/chunks.md'
        with open(relative_path, 'w') as file:
            products = Product.objects.all()

            for product in products:
                file.write(f'## Позиция каталога – {product.name}\n')
                file.write(f'Описание: {product.description.replace('\r','')}\n')
                file.write(f'Цена: {int(product.price)} рублей\n')
 
                file.write(f'Ссылка на товар: [{product.name}](http://127.0.0.1:8000{product.get_absolute_url()})\n\n')

            for category in Category.objects.all():
                chunks = Chunk.objects.filter(category=category)
                for chunk in chunks:
                    file.write(f'## {category.name}\n')
                    file.write(f'{chunk.text}\n')
```

3. Выполнение команды экспорта:

- список доступных команд:

```
python manage.py
```

- выполнение экспорта:

```
python manage.py chunks_export
```

4. Перейти в терминале в каталог api:

```
cd api
```

5. Установка библиотек:

```
pip install -r requirements.txt
```

6. Запускаем FastAPI:

```
uvicorn main:app --reload --host 5000
```
