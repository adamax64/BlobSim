from sqlalchemy import Column, Enum, Integer, BigInteger

from data.db.db_engine import Base
from data.model.policy_type import PolicyType


class Policy(Base):
    __tablename__ = 'policies'
    __table_args__ = {'schema': 'BCS'}

    id = Column(Integer, primary_key=True)
    policy_type = Column(Enum(PolicyType))
    effect_until = Column(BigInteger)
    applied_level = Column(Integer)
