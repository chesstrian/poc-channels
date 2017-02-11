import requests

from lxml import etree


def stock(symbol):
    """
    Get stock quote for a given company symbol

    :param symbol: Company symbol to query in Yahoo! API
    :return: Tuple with first element telling if was an error, and second element with a related message
    """

    api = 'http://finance.yahoo.com/webservice/v1/symbols/{}/quote'
    error = 'Invalid symbol {}'
    message = '{symbol} ({name}) quote is ${price:.2f} per share'

    r = requests.get(api.format(symbol))
    xml = etree.fromstring(r.content)

    count = int(xml.xpath('//resources/@count')[0])
    if count > 0:
        xpath = '//field[@name="{}"]/text()'

        name = xml.xpath(xpath.format('name'))[0]
        price = xml.xpath(xpath.format('price'))[0]
        company_symbol = xml.xpath(xpath.format('symbol'))[0]

        name = name.lower().replace('inc.', 'INC')
        price = float(price)

        return False, message.format(name=name, price=price, symbol=company_symbol)
    else:
        return True, error.format(symbol)


def day_range(symbol):
    """
    Get days low and days high quotes for a given company symbol

    :param symbol: Company symbol to query in Yahoo! API
    :return: Tuple with first element telling if was an error, and second element with a related message
    """

    api = 'http://query.yahooapis.com/v1/public/yql?q={}&env=store://datatables.org/alltableswithkeys'
    error = 'Invalid symbol {}'
    query = 'select * from yahoo.finance.quotes where symbol in ("{}")'
    message = '{symbol} ({name}) Days Low quote is ${low:.2f} and Days High quote is ${high:.2f}'

    r = requests.get(api.format(query.format(symbol)))
    xml = etree.fromstring(r.content)

    try:
        error = xml.xpath('//error/description/text()')[0]
    except IndexError:
        pass
    else:
        return True, error

    name = xml.xpath('//Name/text()')[0]
    if name != '':
        company_symbol = xml.xpath('//quote/@symbol')[0]

        try:
            low = xml.xpath('//DaysLow/text()')[0]
            low = float(low)
        except IndexError:
            low = ''
        try:
            high = xml.xpath('//DaysHigh/text()')[0]
            high = float(high)
        except IndexError:
            high = ''

        name = name.lower().replace('inc.', 'INC')

        return False, message.format(name=name, low=low, high=high, symbol=company_symbol)
    else:
        return True, error.format(symbol)


day_range('TSLA')