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
        'products_on_sale': Product.objects.filter(on_sale=True),
        'products_on_popular': Product.objects.filter(on_popular=True)
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

        # Получение параметров сортировки из запроса
        sort_name = self.request.GET.get('sort_name')
        sort_price = self.request.GET.get('sort_price')

        # Сортировка по имени
        if sort_name == 'asc_name':
            queryset = queryset.order_by('name')
        elif sort_name == 'desc_name':
            queryset = queryset.order_by('-name')

        # Сортировка по цене
        if sort_price == 'asc_price':
            queryset = queryset.order_by('price')
        elif sort_price == 'desc_price':
            queryset = queryset.order_by('-price')

        return queryset

# Определение класса представления для отображения детальной информации о продукте
class ProductDetailView(DetailView):
    # Указание модели, с которой работает представление
    model = Product
    # Шаблон для отображения информации о продукте
    template_name = 'product_detail.html'
    # Имя переменной контекста для продукта в шаблоне
    context_object_name = 'product'
