from datetime import date, datetime, timedelta
from pyluach import dates, hebrewcal, parshios
from pyluach.dates import HebrewDate, GregorianDate
from convertdate import gregorian, julian
from pyluach import dates
from dateutil.relativedelta import relativedelta


class userDate:
    def __init__(self, g_date):
        self.g_date = g_date
        self.h_date = dates.HebrewDate.from_pydate(g_date)

    def print_dates(self):
        print("Foreign date:", self.g_date.strftime("%A, %d %B %Y"))
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

    # def print_reminder(self, next_date):
    #     next_date_python = date(next_date.year, next_date.month, next_date.day)
    #     next_date_minus_month = next_date_python - relativedelta(months=1)
    #     print("Reminder a month ago:",
    #           next_date_minus_month.strftime("%A, %d %B %Y"))


# if __name__ == "__main__":
#     d = userDate(2010, 6, 2)
#     d.print_dates()
#     next_date = d.get_next_date()
#     d.print_reminder(next_date)

# gregorian_date = dates.GregorianDate(2010, 6, 2)
# hebrew_date = gregorian_date.to_heb()
# print("Foreign date:", gregorian_date.strftime("%A, %d %B %Y"))
# print("Hebrew date:", hebrew_date.hebrew_date_string())

# today = dates.HebrewDate.today()
# print("hebrew date today:", today.day, "hebrew date:", hebrew_date.day)

# if today.month <= hebrew_date.month < 7 and today.day <= hebrew_date.day < 30:

#     current_hebrew_year = dates.HebrewDate.today().year
#     next_hebrew_year = current_hebrew_year
#     next_hebrew = dates.HebrewDate(
#         next_hebrew_year, hebrew_date.month, hebrew_date.day)
#     next_date = next_hebrew.to_greg()
#     print("next year :", next_date.strftime("%A, %d %B %Y"))
#     print("next Hebrew year:", next_hebrew.hebrew_date_string())
# else:

#     current_hebrew_year = dates.HebrewDate.today().year
#     next_hebrew_year = current_hebrew_year + 1
#     next_hebrew = dates.HebrewDate(
#         next_hebrew_year, hebrew_date.month, hebrew_date.day)
#     next_date = next_hebrew.to_greg()
#     print("next year :", next_date.strftime("%A, %d %B %Y"))
#     print("next Hebrew year:", next_hebrew.hebrew_date_string())

# next_date_python = date(next_date.year, next_date.month, next_date.day)
# next_date_minus_month = next_date_python - relativedelta(months=1)
# print("Reminder a month ago:",
#       next_date_minus_month.strftime("%A, %d %B %Y"))
# today = date.today()
# print("today is:", today)
# print("day:", today.day)

# print(today.strftime("%A, %d %B %Y"))

# next_year = today.replace(year=today.year + 1)
# print("next year:", next_year)

# difference = abs(next_year-today)
# print("only {} days until next year".format(difference.days))

# AdeleKenan = date(1998, 12, 9)
# print("Adele Kenan was born on:", AdeleKenan)
# print(AdeleKenan.weekday())

# new_date = today + timedelta(days=11*30)
# print("today + 11 month:", new_date)

# passed_away_date = datetime(2022, 6, 11)
# current_date = datetime.now()
# memorial_date_next_year = datetime(
#     current_date.year + 1, passed_away_date.month, passed_away_date.day)
# print("Date plus a year from today:", memorial_date_next_year)


# todayh = dates.HebrewDate.today()
# print("hebrew date today: ", todayh.hebrew_date_string())

# Adele = dates.HebrewDate(5759, 9, 20)
# print(Adele.hebrew_date_string())
