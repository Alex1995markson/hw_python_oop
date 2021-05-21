import datetime as dt
from datetime import timedelta  # Refactor
from typing import Optional


class Calculator:
    date_format = '%Y-%m-%d'

    def __init__(self, limit):
        self.limit = limit
        self.records = list()

    def add_record(self, Record):
        '''Создание логики добавления новой покупки или калории в records'''
        self.records.append(Record)

    def get_today_stats(self):
        ''' Определяем сколько еще может быть потрачено сегодня денег '''
        today_i = returnTodayDate()
        sum_day = 0
        for item in range(len(self.records)):
            if today_i == self.records[item].date:
                sum_day += self.records[item].amount

        return sum_day

    def get_week_stats(self):
        ''' Вычисление потребляемых/потраченных калорий/денежных средств '''
        sum_of_week = 0
        week = startWeek(today_i)
        today_i = dt.date.today().strftime(self.date_format)
        start_W = startWeek(today_i)
        start_date = dt.datetime.strptime(start_W, self.date_format)
        end_date = dt.datetime.strptime(today_i, self.date_format)
        delta = timedelta(days=1)
        while start_date <= end_date:
            today_f = returnTodayDate(start_date)
            for item in range(len(self.records)):
                if today_f == self.records[item].date:
                    sum_of_week += self.records[item].amount
            start_date += delta
        return sum_of_week


class CashCalculator(Calculator):
    EURO_RATE = 73.53
    USD_RATE = 89.82

    def __init__(self, limit):
        super().__init__(limit)

    def show(self):
        ''' Показать лимит по операции '''
        print('Limit for operation is', len(self.records))

    def get_currency(self, currency):
        ''' Вычисление текущей суммы '''
        if currency == 'rub':
            money_currency = super().get_today_stats()
            res = self.limit - money_currency
            return res
        elif currency == 'usd':
            money_currency = super().get_today_stats() / self.USD_RATE
            res = (self.limit / self.USD_RATE - money_currency)
            return res
        elif currency == 'eur':
            money_currency = super().get_today_stats() / self.EURO_RATE
            res = (self.limit / self.EURO_RATE - money_currency)
            return res
        else:
            return 'None'

    def get_today_cash_remained(self, currency):
        ''' Показать отстаток в валюте из перечисленных rub, euro, usd '''
        comment = {
            'rub': 'руб',
            'eur': 'Euro',
            'usd': 'USD'
        }
        res = self.get_currency(currency)
        if res > 0:
            return f'На сегодня осталось {round(res, 2)} {comment[currency]}'
        elif res == 0:
            return 'Денег нет, держись'
        elif res < 0:
            return 'Денег нет, держись: твой долг - ' \
                f'{round(abs(res), 2)} {comment[currency]}'


class CaloriesCalculator(Calculator):

    def __init__(self, limit):
        super().__init__(limit)

    def show(self):
        print('Limit for operation is', self.limit)

    def get_calories_remained(self):
        ''' Показать остаток по калориям на текущий день '''
        sum_of_day = super().get_today_stats()
        if self.limit - sum_of_day > 0:
            return 'Сегодня можно съесть что-нибудь ещё, но с ' \
                f'общей калорийностью не более {self.limit - sum_of_day} кКал'
        else:
            return 'Хватит есть!'


class Record:
    date_format = '%d.%m.%Y'
    today = dt.datetime.now().strftime(date_format)

    def __init__(self, amount, comment, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        self.date = dt.datetime.strptime(date, self.date_format).date()


def startWeek(current):
    ''' Определяем дату начала недели от заданной (то есть 7 дней назад) '''
    dtc = dt.datetime.strptime(current, '%Y-%m-%d')
    start = dtc - timedelta(days=7)
    return start.strftime("%Y-%m-%d")


def returnTodayDate(day=0, format="%Y-%m-%d"):
    if day == 0:
        todayD = dt.date.today().strftime(format)
    else:
        todayD = day.strftime(format)
    todayD = dt.datetime.strptime(todayD, format).date()
    return todayD
