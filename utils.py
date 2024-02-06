import requests
from lxml import etree
from config import keys

class APIException(Exception):
    pass
class CurrencyConverter:

    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_ticker = keys[quote.lower()]
            base_ticker = keys[base.lower()]
        except KeyError as e:
            raise APIException(f"Валюта {e.args[0]} не найдена!")

        if quote_ticker == base_ticker:
            raise APIException("Нельзя конвертировать валюту саму в себя!")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}!")

        response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
        if response.status_code != 200:
            raise APIException("Ошибка API Центрального Банка России.")

        currency_data = etree.fromstring(response.content)
        valute_dict = {valute.find('CharCode').text: valute for valute in currency_data.findall('Valute')}

        if quote_ticker not in valute_dict or base_ticker not in valute_dict:
            raise APIException("Не удалось найти одну из указанных валют.")

        try:
            quote_value = float(valute_dict[quote_ticker].find('Value').text.replace(",", "."))
            quote_nominal = float(valute_dict[quote_ticker].find('Nominal').text.replace(",", "."))
            base_value = float(valute_dict[base_ticker].find('Value').text.replace(",", "."))
            base_nominal = float(valute_dict[base_ticker].find('Nominal').text.replace(",", "."))
        except Exception as e:
            raise APIException(f"Не удалось обработать курс валюты: {e}")

        result = (quote_value / quote_nominal) * amount * (base_nominal / base_value)

        return result