import requests
import json
from config import keys


class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        
        if quote == base:
            raise ConvertionException('Unable to transfer identical currencies {base}.')
        
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException('We were unable to process {quote} currency.')
        
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException('We were unable to process {base} currency.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('We were unable to process the quantity {amount}.')
        
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym{quote_ticker}&tsym{base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base