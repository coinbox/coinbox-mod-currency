import cbpos

import cbpos.mod.base.models.common as common

from sqlalchemy import func, Table, Column, Integer, Numeric, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

import babel.numbers

CurrencyValue = lambda: Numeric(10, 4)

class Currency(cbpos.database.Base, common.Item):
    __tablename__ = 'currencies'

    id = Column(String(3), primary_key=True)

    @hybrid_property
    def name(self):
        return babel.numbers.get_currency_name(self.id, locale=cbpos.locale)

    @hybrid_property
    def symbol(self):
        return babel.numbers.get_currency_symbol(self.id, locale=cbpos.locale)

    @hybrid_property
    def display(self):
        return babel.numbers.get_currency_name(self.id, locale=cbpos.locale)

    @hybrid_property
    def current_rate(self):
        return self.rates[0]
    
    @current_rate.setter
    def current_rate(self, rate):
        self.rates.append(rate)
        self.update()

    def __repr__(self):
        return "<Currency %s>" % (self.symbol,)

    def format(self, value):
        return babel.numbers.format_currency(value, self.id)
