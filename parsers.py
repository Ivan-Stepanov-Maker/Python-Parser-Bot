import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

CATEGORIES = {
    'tech': {
        'wb': 'https://www.wildberries.ru/catalog/0/search.aspx?search=техника',
        'ozon': 'https://www.ozon.ru/search/?text=техника&from_global=true'
    },
    'shirt': {
        'wb': 'https://www.wildberries.ru/catalog/0/search.aspx?search=Одежда',
        'ozon': 'https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=одежда'
    },
    'toof': {
        'wb': 'https://www.wildberries.ru/catalog/0/search.aspx?search=обувь',
        'ozon': 'https://www.ozon.ru/category/obuv-17777/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=обувь'
    },
    'tshirt': {
        'wb': 'https://www.wildberries.ru/catalog/0/search.aspx?search=футболки',
        'ozon': 'https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=футболки'
    },
    'pants': {
        'wb': 'https://www.wildberries.ru/catalog/0/search.aspx?search=штаны',
        'ozon': 'https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=штаны'
    },
    'akssesuars': {
        'wb': 'https://www.wildberries.ru/catalog/0/search.aspx?search=аксесуары',
        'ozon': 'https://www.ozon.ru/category/aksessuary-7697/?category_was_predicted=true&deny_category_prediction=true&from_global=true&text=акссесуары'
    },
    'man_surprace': {
        'wb': 'https://www.wildberries.ru/catalog/0/search.aspx?search=Подарки%20для%20мужчин',
        'ozon': 'https://www.ozon.ru/search/?text=подарки+для+мужчин&from_global=true'
    },
    'woman_surpace': {
        'wb': 'https://www.wildberries.ru/catalog/0/search.aspx?search=Подарки%20для%20женщин',
        'ozon': 'https://www.ozon.ru/search/?text=подарки+для+женщин&from_global=true'
    },
    'child_surpace': {
        'wb': 'https://www.wildberries.ru/catalog/0/search.aspx?search=Подарки%20для%20детей',
        'ozon': 'https://www.ozon.ru/search/?text=подарки+для+детей&from_global=true'
    },
    'sport': {
        'wb': 'https://www.wildberries.ru/catalog/0/search.aspx?search=спорт',
        'ozon': 'https://www.ozon.ru/search/?text=спорт&from_global=true'
    },
    'book': {
        'wb': 'https://www.wildberries.ru/catalog/0/search.aspx?search=книги',
        'ozon': 'https://www.ozon.ru/category/biznes-literatura-40024/'
    }
}

def parse_wb_product(url):
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    })
    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлекаем названия товаров
    products = []
    for item in soup.find_all('div', class_='product-card j-card-item'):
        title = item.find('span', {'data-hook': 'product-title'})
        price = item.find('ins', class_='lower-price')
        article = item.find('meta', attrs={'itemprop': 'sku'})

        stock = None  # Количество на складе может отсутствовать или отображаться иначе

        if title and price and article:
            product = {
                'title': title.text.strip(),
                'price': float(price.text.replace(' ', '').replace(',', '.').strip()),
                'article': article['content'],
                'stock': stock
            }
            products.append(product)

    return products


def parse_ozon_product(url):
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    })
    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлекаем названия товаров
    products = []
    for item in soup.find_all('div', class_='tile'):
        title = item.find('h3', class_='tile__title')
        price = item.find('span', class_='tile__price')
        article = item.find('input', attrs={'name': 'productId'})

        stock = None  # Озон не показывает наличие товара сразу на странице результатов поиска

        if title and price and article:
            product = {
                'title': title.text.strip(),
                'price': float(price.text.split()[0].replace('₽', '').replace(' ', '')),
                'article': article['value'],
                'stock': stock
            }
            products.append(product)

    return products