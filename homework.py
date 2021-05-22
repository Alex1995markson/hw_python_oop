import datetime as dt
from typing import Optional, Dict


class Calculator:
    date_format: str = '%Y-%m-%d'
    delta_week: dt = dt.timedelta(days=7)

    def __init__(self, limit: float):
        self.limit = limit
        self.records = list()

    def add_record(self, Record) -> None:
        '''Создание логики добавления новой покупки или калории в records'''
        self.records.append(Record)

    def get_today_stats(self) -> float:
        ''' Определяем сколько еще может быть
            потрачено сегодня денег/калорий '''
        today_i = returnTodayDate()
        sum_day: float = 0
        for item in range(len(self.records)):
            if today_i == self.records[item].date:
                sum_day += self.records[item].amount
        return sum_day

    def get_week_stats(self) -> float:
        '''  Считает сколько денег/
            калорий потрачено за последние 7 дней '''
        today: dt = dt.date.today()
        delta_week: dt = dt.timedelta(days=7)
        delta_week: dt = today - delta_week
        return sum(
            item.amount for item in self.records if
            delta_week < item.date <= today)


class CashCalculator(Calculator):
    EURO_RATE: float = 73.53  # Курс евро
    USD_RATE: float = 89.82  # Курс доллара

    def __init__(self, limit):
        super().__init__(limit)

    def show(self) -> None:
        ''' Показать лимит по операции '''
        print('Limit for operation is', len(self.records))

    def get_currency(self, currency: str) -> float:
        ''' Вычисление текущей суммы '''
        money_currency = super().get_today_stats()
        if currency == 'rub':
            res = self.limit - money_currency
            return res
        elif currency == 'usd':
            money_currency /= self.USD_RATE
            res = (self.limit / self.USD_RATE - money_currency)
            return res
        elif currency == 'eur':
            money_currency /= self.EURO_RATE
            res = (self.limit / self.EURO_RATE - money_currency)
            return res
        else:
            return 'None'

    def get_today_cash_remained(self, currency: str) -> str:
        ''' Показать отстаток в валюте из перечисленных rub, euro, usd '''
        comment: Dict[str, str] = {
            'rub': 'руб',
            'eur': 'Euro',
            'usd': 'USD'
        }
        res = self.get_currency(currency)
        if res > 0:
            return f'На сегодня осталось {round(res,2)} {comment[currency]}'
        elif res == 0:
            return 'Денег нет, держись'
        elif res < 0:
            return 'Денег нет, держись: твой долг - ' \
                f'{round(abs(res),2)} {comment[currency]}'


class CaloriesCalculator(Calculator):

    def __init__(self, limit):
        super().__init__(limit)

    def show(self) -> None:
        ''' Показать лимит по калориям '''
        print('Limit for operation is', self.limit)

    def get_calories_remained(self) -> str:
        ''' Показать остаток по калориям на текущий день '''
        sum_of_day: float = super().get_today_stats()
        res: float = self.limit - sum_of_day
        if res > 0:
            return 'Сегодня можно съесть что-нибудь ещё, но с ' \
                f'общей калорийностью не более {res} кКал'
        else:
            return 'Хватит есть!'


class Record:
    date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.date_format).date()


def startWeek(current) -> str:
    ''' Определяем дату начала недели от заданной (то есть 7 дней назад) '''
    dtc = dt.datetime.strptime(current, '%Y-%m-%d')
    start = dtc - dt.timedelta(days=7)
    return start.strftime("%Y-%m-%d")


def returnTodayDate(day=0, format="%Y-%m-%d") -> dt:
    if day == 0:
        todayD = dt.date.today().strftime(format)
    else:
        todayD = day.strftime(format)
    todayD = dt.datetime.strptime(todayD, format).date()
    return todayD
