from database import Base
from sqlalchemy import Column, Integer, String, Boolean, BigInteger

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    address_id = Column(Integer, nullable=True)
    workplace = Column(String, nullable=True)
    birth_date = Column(String, nullable=True)
    passport_series = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)

    def __init__(self, telegram_id: int, full_name: str = None, address_id: int = None,
                 workplace: str = None, birth_date: str = None,
                 passport_series: str = None, phone_number: str = None,
                 project_id: int = None):
        self.telegram_id = telegram_id
        self.full_name = full_name
        self.address_id = address_id
        self.workplace = workplace
        self.birth_date = birth_date
        self.passport_series = passport_series
        self.phone_number = phone_number
        self.project_id = project_id

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, full_name={self.full_name})>"
        