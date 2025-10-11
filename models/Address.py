from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, nullable=True)
    district_id = Column(Integer, nullable=True)
    neighborhood = Column(String, nullable=True)
    user_id = Column(Integer, nullable=True)

    def __init__(self, region_id: int = None, district_id: int = None, neighborhood: str = None):
        self.region_id = region_id
        self.district_id = district_id
        self.neighborhood = neighborhood

    def __repr__(self):
        return f"<Address(region_id={self.region_id}, district_id={self.district_id}, neighborhood={self.neighborhood})>"