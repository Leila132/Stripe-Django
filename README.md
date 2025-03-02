# Cafe-Order-Management-System-Django-

Веб-приложение, разработанное на Django с использованием Django REST Framework для оплаты заказов и товаров (использование библиотеки Stripe)

## Установка

1. Клонируйте репозиторий:

`git clone https://github.com/Leila132/Stripe-Django.git`

2. Перейдите в директорию проекта:

`cd Stripe-Django`

3. Установите зависимости:

`pip install -r requirements.txt`

4. Установите переменную:

`export stripe_api_key=sk_test_4eC39HqLyjWDarjtT1zdp7dc`

5. Проведите миграции:

`python manage.py migrate`

6. Создайте суперпользователя:

`python manage.py createsuperuser`

## Запуск

Чтобы запустить проект, выполните:

`python manage.py runserver`

## Использование

Для взаимодействия с товарами перейдите на панель администратора и создайте товары, виды скидок и налогов, заказы.

Модель товара: название, описание, есть возможность выбрать валюту для цены.

Модель скидки: включает в себа название, сумму скидки и валюту.

Модель налога: включает в себа название, процент налога и валюту.

Модель заказа: можно выбрать товары, использовать доступную скидку, добавить налог. При создании или изменении заказа пересчитывается итоговая стоимость по формуле: "изначальная сумма выбранных товаров" - "выбранная скидка" + "добавление налога", который высчитывается как процент от суммы после вычета скидки.

## API

- `GET /buy/1` Stripe Session get id of Item 1
- `GET /buy-order/1` Stripe Session get id of Order 1
- `GET /buy2/1` Stripe Payment Intent get id of Item 1
- `GET /buy2-order/1` Stripe Payment Intent get id of Order 1
- `GET /item/1` Pay Item 1
- `GET /order/1` Pay Order 1

По адресу /item/1 и /order/1 находятся две кнопки: "Buy with Checkout", которая производит редирект на Checkout форму, и "Pay with Card", колторая открывает собственную форму для заполнения данных о карте.