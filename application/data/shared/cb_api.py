import requests
import dateutil.parser
import xml.etree.ElementTree as ET


def get_rubles(currency: str, published_at: str):
    if currency == "RUR":
        return 1.0

    dttm = dateutil.parser.isoparse(published_at)
    year = dttm.year
    month = dttm.month

    # Обработка неправильных данных в файле
    if (year == 2016 and month <= 6 or year < 2016) and currency == "BYN":
        currency = "BYR"
    if (year == 2016 and month > 6 or year >= 2017) and currency == "BYR":
        currency = "BYN"
    if (year < 2023 or year == 2023 and month == 1) and currency == "GEL":
        year = 2023
        month = 2

    if year not in currencies_by_date:
        currencies_by_date[year] = {
            month: {
                currency: get_currency_from_cb(currency, month, year)
            }
        }
    if month not in currencies_by_date[year]:
        currencies_by_date[year][month] = {
            currency: get_currency_from_cb(currency, month, year)
        }
    if currency not in currencies_by_date[year][month]:
        currencies_by_date[year][month][currency] = get_currency_from_cb(currency, month, year)

    return currencies_by_date[year][month][currency]


def make_request(date):
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    return requests.get(url)


def get_currency_from_cb(currency: str, month: int, year: int):
    print(currency, month, year)
    month = "0" + str(month) if month < 10 else month
    date = f"01/{month}/{year}"
    response = make_request(date)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        valute = root.find(f".//Valute[CharCode='{currency}']")

        if valute is not None:
            multiplier = float(valute.find('VunitRate').text.replace(",", "."))
            return multiplier
    else:
        return get_currency_from_cb(currency, month, year)


currencies_by_date = {}