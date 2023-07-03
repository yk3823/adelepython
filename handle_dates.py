from datetime import date, datetime, timedelta
from pyluach import dates, hebrewcal, parshios
from pyluach.dates import HebrewDate, GregorianDate
from convertdate import gregorian, julian
from pyluach import dates
from dateutil.relativedelta import relativedelta


class userDate:
    def __init__(self, datafromusercall):
        # trying to give an example like you got a date from type date from the user
        self.rdate = datetime.strptime(
            datafromusercall.get('date'), "%d/%m/%Y")
        self.h_date = dates.HebrewDate.from_pydate(self.rdate)
        self.fullname = datafromusercall.get('fullname')
        self.date_of_death = datetime.strptime(
            datafromusercall.get('date_of_death'))
        self.date_next = datafromusercall.get('date_next')
        self.date_reminder = datafromusercall.get('date_reminder')
        self.user_id = datafromusercall.get('user_id')
        self.image = datafromusercall.get('image')

    def print_dates(self):
        print("Foreign date:", self.rdate.strftime('%A, %d %B %Y'))
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

    def validate_input(self):
        if None in [self.fullname, date_of_death, date_next, date_reminder, self.user_id, self.image_id]:
            return jsonify({"error": "Missing data fields"}), 400
        try:
            date_of_death = datetime.strptime(date_of_death, '%Y-%m-%d')
            date_next = datetime.strptime(date_next, '%Y-%m-%d')
            date_reminder = datetime.strptime(date_reminder, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400
