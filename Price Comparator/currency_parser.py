def price_converter(price, curr_rates, to_currency, from_huf=True):    
    for currency in curr_rates:
        if currency["name"] == to_currency:
            currency_exchange_rate = float(currency["rate"])
    if from_huf:
        item_price = round(float(price) / currency_exchange_rate, 2)
        return item_price
    else:
        item_price = round(currency_exchange_rate * float(price), 0)
        return int(item_price)