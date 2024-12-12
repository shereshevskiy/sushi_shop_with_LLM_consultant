from django.db import models
from django.urls import reverse


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    on_sale = models.BooleanField(default=False)  # Новое поле "товар по акции"
    on_popular = models.BooleanField(default=False)  # Новое поле "популярная продукция"

    def __str__(self) -> str:
        """Returns the string representation of the Product instance, which is the product's name."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the URL to access a particular product instance.
        
        :return: URL to access the product instance
        """
        return reverse('product_detail', args=[str(self.pk)])
