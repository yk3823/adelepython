from datetime import date, datetime, timedelta
from pyluach import dates, hebrewcal, parshios
from pyluach.dates import HebrewDate, GregorianDate
from convertdate import gregorian, julian
from pyluach import dates
from dateutil.relativedelta import relativedelta

    
class userDate:
    def __init__(self,datafromusercall):
      
        self.data = datafromusercall
        self.h_date = dates.HebrewDate.from_pydate(datafromusercall)
        self.fullname = datafromusercall.get('fullname')
        self.date_of_death = datafromusercall.get('date_of_death')
        self.date_next = datafromusercall.get('date_next')
        self.date_reminder = datafromusercall.get('date_reminder')
        self.user_id = datafromusercall.get('user_id')

    def print_dates(self):
        print("Foreign date:", self.datafromusercall.strftime("%A, %d %B %Y"))
        print("Hebrew date:", self.h_date.hebrew_date_string())

    def get_next_date(self):
        today = dates.HebrewDate.today()

        if today.month <= self.h_date.month < 7 and today.day <= self.h_date.day < 30:
            next_hebrew_year = today.year
        else:
            next_hebrew_year = today.year + 1

        next_hebrew = dates.HebrewDate(
            next_hebrew_year, self.h_date.month, self.h_date.day)
        next_date = next_hebrew.to_greg()

        print("next year :", next_date.strftime("%A, %d %B %Y"))
        print("next Hebrew year:", next_hebrew.hebrew_date_string())
        return next_date

    def print_reminder(self, next_date):
        next_date_minus_month = next_date - relativedelta(months=1)
        print("Reminder a month ago:",
              next_date_minus_month.strftime("%A, %d %B %Y"))

