from django.db import models
from django.core.validators import MinValueValidator

DEFAULT_CATEGORY = 'other'
CATEGORY_CHOICES = (
    (DEFAULT_CATEGORY, 'Разное'),
    ('food', 'Еда'),
    ('tech', 'Бытовая техника'),
    ('tools', 'Инструменты'),
    ('toys', 'Игрушки'),
)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    category = models.CharField(max_length=20, default=DEFAULT_CATEGORY, choices=CATEGORY_CHOICES,
                                verbose_name='Категория')
    amount = models.IntegerField(verbose_name='Остаток', validators=(MinValueValidator(0),))
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2,
                                validators=(MinValueValidator(0),))

    def __str__(self):
        return f'{self.name} - {self.amount}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']


#
# class ProductOrder(models.Model):
#     product_qty = models.IntegerField(max_length=100, verbose_name='Количество товаров')
#     order = models.ForeignKey('webapp.Order', related_name='orders', on_delete=models.CASCADE, verbose_name='Заказ')
#     product = models.ForeignKey('webapp.Product', related_name='products', on_delete=models.CASCADE,
#                                 verbose_name='Товар')
#
# class Order(models.Model):
#     user_name = models.CharField(max_length=100, verbose_name='Имя пользователя')
#     phone = models.IntegerField(max_length=100, verbose_name='Телефон')
#     product_name = models.CharField(max_length=100, verbose_name='Название продукта')
