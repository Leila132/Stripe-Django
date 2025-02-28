from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from model_utils import FieldTracker

# 1USD=100RUB
MONEY_C = 100

class Discount(models.Model):
    name = models.CharField('Название скидки', max_length=100)
    amount = models.DecimalField('Сумма скидки', max_digits=10, decimal_places=2)
    is_active = models.BooleanField('Активна', default=True)
    currency = models.CharField('Валюта', max_length=3, choices=[
        ('USD', 'USD'),
        ('RUB', 'RUB')
    ], default='RUB')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

class Tax(models.Model):
    name = models.CharField('Название налога', max_length=100)
    rate = models.DecimalField('Ставка налога', max_digits=5, decimal_places=2)
    is_active = models.BooleanField('Активен', default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'

class Item(models.Model):
    name = models.CharField('Название', max_length=50)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField('Валюта', max_length=3, choices=[
        ('USD', 'USD'),
        ('RUB', 'RUB')
    ], default='RUB')
    id = models.AutoField(primary_key=True)

    tracker = FieldTracker(['price', 'currency'])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Order(models.Model):
    items = models.ManyToManyField(
        Item,
        related_name='orders',
        verbose_name='Товары'
    )
    discount = models.ForeignKey(
        Discount, 
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Скидка'
    )

    taxes = models.ManyToManyField(
        Tax,
        blank=True,
        verbose_name='Налоги'
    )
    subtotal = models.DecimalField('Стоимость до скидок и налогов', max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField('Сумма скидки', max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField('Сумма налогов', max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField('Общая стоимость', max_digits=10, decimal_places=2, default=0)

    currency = models.CharField('Валюта', max_length=3, choices=[
        ('USD', 'USD'),
        ('RUB', 'RUB')
    ], default='RUB')

    def calculate_total_price(self):
        """
        Вычисляет общую стоимость заказа с учетом скидок и налогов
        """
        # Базовая стоимость товаров
        self.subtotal = 0
        for item in self.items.all():
            price = 0
            if item.currency == self.currency:
                price = float(item.price)
            else:
                if self.currency == 'USD':
                    price = round(float(item.price) / MONEY_C, 2)
                else: 
                    price = round(float(item.price) * MONEY_C, 2)
            self.subtotal += price
        
        # Округляем subtotal до двух знаков
        self.subtotal = round(self.subtotal, 2)

        self.discount_amount = 0
        if self.discount:
            discount_value = float(self.discount.amount)
            if self.discount.currency != self.currency:
                if self.currency == 'USD':
                    discount_value = round(discount_value / MONEY_C, 2)
                else:
                    discount_value = round(discount_value * MONEY_C, 2)
            
            self.discount_amount = round(min(discount_value, self.subtotal), 2)
        
        after_discount = round(self.subtotal - self.discount_amount, 2)
        
        self.tax_amount = 0
        if self.id:  
            for tax in self.taxes.filter(is_active=True):
                tax_value = round(after_discount * float(tax.rate) / 100, 2)
                self.tax_amount += tax_value
        
        # Округляем tax_amount до двух знаков
        self.tax_amount = round(self.tax_amount, 2)
        
        self.price = round(after_discount + self.tax_amount, 2)
        return self.price
        
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

@receiver(m2m_changed, sender=Order.items.through)
@receiver(m2m_changed, sender=Order.taxes.through)
@receiver(post_save, sender=Order)
def update_total_price(sender, instance, **kwargs):
    """
    Сигнал для пересчета общей стоимости заказа при изменении блюд, налогов или скидки.
    """
    # Определяем, какой сигнал сработал
    if 'action' in kwargs:  # Для m2m_changed
        if kwargs['action'] not in ['post_add', 'post_remove', 'post_clear']:
            return
        instance.price = instance.calculate_total_price()
        instance.save()
    else:  # Для post_save
        update_fields = kwargs.get('update_fields')
        if not update_fields or 'discount' in update_fields:
            instance.price = instance.calculate_total_price()
            instance.save(update_fields=['subtotal', 'discount_amount', 'tax_amount', 'price'])

@receiver(post_save, sender=Item)
def update_orders_on_item_price_change(sender, instance, **kwargs):
    """
    Сигнал для пересчета стоимости всех заказов, содержащих товар,
    цена которого изменилась.
    """
    # Получаем все заказы, содержащие этот товар
    orders = Order.objects.filter(items=instance)
    
    # Обновляем цену для каждого заказа
    for order in orders:
        order.price = order.calculate_total_price()
        order.save(update_fields=['subtotal', 'discount_amount', 'tax_amount', 'price'])