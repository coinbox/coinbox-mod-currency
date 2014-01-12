import cbpos

import cbpos.mod.base.models.common as common

from sqlalchemy import func, Table, Column, Integer, Numeric, String, Float, Boolean, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

from cbpos.mod.currency.models.currency import CurrencyValue

class CurrencyUnit(cbpos.database.Base, common.Item):
    __tablename__ = 'currency_units'

    #__table_args__ = (
    #    UniqueConstraint('currency_id', 'value'),
    #)

    id = Column(Integer, primary_key=True)
    currency_id = Column(String(3), ForeignKey('currencies.id'))
    value = Column(CurrencyValue(), nullable=False)

    currency = relationship("Currency", order_by="Currency.id", backref="units")

    @hybrid_property
    def display(self):
        return self.currency.format(self.value)

    def __lt__(self, other):
        if other.currency != self.currency:
            from cbpos.mod.currency.controllers import convert
            other_value = convert(other.value, other.currency, self.currency)
        else:
            other_value = other.value
        return self.value<other_value

    def __repr__(self):
        return "<CurrencyUnit %s>" % (self.currency.format(self.value),)
