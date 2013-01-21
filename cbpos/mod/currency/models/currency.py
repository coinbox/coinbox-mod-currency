import cbpos

import cbpos.mod.base.models.common as common

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

class Currency(cbpos.database.Base, common.Item):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    symbol = Column(String(5), nullable=False, unique=True)
    value = Column(Float, nullable=False)
    decimal_places = Column(Integer, nullable=False, default=2)
    digit_grouping = Column(Boolean, default=False)

    @hybrid_property
    def display(self):
        return self.name
    
    @display.expression
    def display(self):
        return self.name

    def __repr__(self):
        return "<Currency %s>" % (self.symbol,)

    def getFormatString(self):
        return (',' if self.digit_grouping else '')+\
               ('.%df' % (max(0, self.decimal_places),))

    def format(self, value):
        return '%s %s' % (format(round(value, max(0, self.decimal_places)), self.getFormatString()), self.symbol)
