from django.core.management.base import BaseCommand
from neuro_assistant.models import Category, Chunk
from shop.models import Product


class Command(BaseCommand):
    help = 'Export all chunks to a text file'

    def handle(self, *args, **options):
        relative_path = '../api/chunks.md'
        with open(relative_path, 'w', encoding='utf-8') as file:
            products = Product.objects.all()

            # экспорт товаров
            for product in products:
                file.write(f'## Позиция каталога – {product.name}\n')
                file.write(f'Описание: {product.description.replace('\r','')}\n')
                file.write(f'Цена: {int(product.price)} рублей\n')
                file.write(f'Ссылка на товар: [{product.name}](http://127.0.0.1:8000{product.get_absolute_url()})\n\n')

            # экспорт категорий
            for category in Category.objects.all():
                chunks = Chunk.objects.filter(category=category)
                for chunk in chunks:
                    file.write(f'## {category.name}\n')
                    file.write(f'{chunk.text}\n')
