
import datetime
import uuid
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['memorial_site']


class User:
    def __init__(self, first_name: str, last_name: str, email: str, password: str):
        self.user_id = uuid.uuid4().hex
        self.fname = first_name
        self.last = last_name
        self.email = email
        self.password = password
        self.created_at = datetime.datetime.utcnow()

    def __repr__(self):
        return f'<User {self.name}>'


class Deceased:
    def __init__(self, fullname: str, date_of_birth: datetime, date_of_death: datetime, date_death_year: datetime, date_death_11month: datetime, user_id: str):
        self.deceased_id = uuid.uuid4().hex
        self.fullname = fullname
        self.date_of_death = date_of_death
        self.date_death_year = date_death_year
        self.date_death_11month = date_death_11month
        self.user_id = user_id
        self.created_at = datetime.datetime.utcnow()

    def __repr__(self):
        return f'<Deceased {self.name}>'


class Group:
    def __init__(self, fullname: str, description: str, user_id: str):
        self.group_id = uuid.uuid4().hex
        self.fullname = fullname
        self.description = description
        self.user_id = user_id
        self.created_at = datetime.datetime.utcnow()

    def __repr__(self):
        return f'<Group {self.name}>'
