import datetime as dt
from typing import Optional, Dict, List


class Calculator:
    delta_week: dt.timedelta = dt.timedelta(days=7)

    def __init__(self, limit: float):
        self.limit = limit
        self.records: List = []

    def add_record(self, Record) -> None:
        '''Создание логики добавления новой покупки или калории в records'''
        self.records.append(Record)

    def get_today_stats(self) -> float:
        ''' Определяем сколько еще может быть
            потрачено сегодня денег/калорий '''
        today_i = dt.date.today()
        return sum(
            item.amount for item in self.records if
            today_i == item.date)

    def get_week_stats(self) -> float:
        '''  Считает сколько денег/
            калорий потрачено за последние 7 дней '''
        today: dt.date = dt.date.today()
        delta_week: dt.date = today - dt.timedelta(days=7)
        return sum(
            item.amount for item in self.records if
            delta_week < item.date <= today)


class CashCalculator(Calculator):
    EURO_RATE: float = 73.53
    USD_RATE: float = 89.82

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency: str) -> str:
        ''' Показать отстаток в валюте из перечисленных rub, euro, usd '''
        comment: Dict[str, List] = {
            'rub': ['руб', 1],
            'eur': ['Euro', self.EURO_RATE],
            'usd': ['USD', self.USD_RATE]
        }
        try:
            money_currency = self.get_today_stats() / comment[currency][1]
            res = self.limit / comment[currency][1] - money_currency

            if res > 0:
                return f'На сегодня осталось ' \
                    f'{round(res,2)} {comment[currency][0]}'
            elif res == 0:
                return 'Денег нет, держись'
            elif res < 0:
                return 'Денег нет, держись: твой долг - ' \
                    f'{round(abs(res),2)} {comment[currency][0]}'
        except Exception as e:
            print(f'Неожиданная ошибка проверьтеесть ли такая валюта: {e}')
        return 'Error'


class CaloriesCalculator(Calculator):

    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self) -> str:
        ''' Показать остаток по калориям на текущий день '''
        sum_of_day: float = self.get_today_stats()
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
