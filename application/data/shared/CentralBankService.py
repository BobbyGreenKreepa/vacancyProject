import requests
import dateutil.parser
import xml.etree.ElementTree as ET


class CentralBankService:
    def __init__(self):
        self.currencies_by_date = {}

    def get_rubles(self, currency: str, published_at: str):
        if currency == "RUR":
            return 1.0

        dttm = dateutil.parser.isoparse(published_at)
        year = dttm.year
        month = dttm.month

        if (year == 2016 and month <= 6 or year < 2016) and currency == "BYN":
            currency = "BYR"
        if (year == 2016 and month > 6 or year >= 2017) and currency == "BYR":
            currency = "BYN"
        if (year < 2023 or year == 2023 and month == 1) and currency == "GEL":
            year = 2023
            month = 2

        if year not in self.currencies_by_date:
            self.currencies_by_date[year] = {
                month: {
                    currency: self.get_currency_from_cb(currency, month, year)
                }
            }
        if month not in self.currencies_by_date[year]:
            self.currencies_by_date[year][month] = {
                currency: self.get_currency_from_cb(currency, month, year)
            }
        if currency not in self.currencies_by_date[year][month]:
            self.currencies_by_date[year][month][currency] = self.get_currency_from_cb(currency, month, year)

        return self.currencies_by_date[year][month][currency]

    def make_request(self, date):
        url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
        return requests.get(url)

    def get_currency_from_cb(self, currency: str, month: int, year: int):
        print(currency, month, year)
        month_str = f"0{month}" if month < 10 else str(month)
        date = f"01/{month_str}/{year}"
        response = self.make_request(date)

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            valute = root.find(f".//Valute[CharCode='{currency}']")

            if valute is not None:
                multiplier = float(valute.find('VunitRate').text.replace(",", "."))
                return multiplier
        else:
            return self.get_currency_from_cb(currency, month, year)


central_bank_service = CentralBankService()