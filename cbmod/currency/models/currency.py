import cbpos

import cbpos.mod.base.models.common as common

logger = cbpos.get_logger(__name__)

from sqlalchemy import func, Table, Column, Integer, Numeric, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

import babel.numbers

import sqlalchemy.types as types
from sqlalchemy.dialects.sqlite.base import SQLiteDialect

try:
    from cdecimal import Decimal
except ImportError:
    from decimal import Decimal
    logger.warn('cdecimal not available. Using the regular decimal Decimal class')
else:
    logger.log('Using the cdecimal Decimal class')

class CurrencyValue(types.TypeDecorator):
    """
    Store all currency values (prices, taxes, money) as Numeric data types to keep optimal precision
    Taken and modified from http://stackoverflow.com/a/10386911/1043456
    Since SQLite does not have native support for Decimal data types,
    this TypeDecorator implements either a Numeric data type or a String data type,
    depending on the backend.
    """
    impl = types.TypeEngine
    
    def is_sqlite(self, dialect):
        """
        Returns true if the given dialect is any SQLite dialect.
        """
        return isinstance(dialect, SQLiteDialect)
    
    def load_dialect_impl(self, dialect):
        if self.is_sqlite(dialect):
            return dialect.type_descriptor(types.VARCHAR(100))
        else:
            return dialect.type_descriptor(types.Numeric(10, 4))
    
    def process_bind_param(self, value, dialect):
        if self.is_sqlite(dialect):
            return unicode(value)
        else:
            return value
    
    def process_result_value(self, value, dialect):
        if self.is_sqlite(dialect):
            try:
                return Decimal(value)
            except:
                return None
        else:
            return value

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
        return self.rates.first()
    
    @current_rate.setter
    def current_rate(self, rate):
        self.rates.append(rate)

    def __repr__(self):
        return "<Currency %s>" % (self.id,)

    def format(self, value):
        return babel.numbers.format_currency(value, self.id, locale=cbpos.locale)
