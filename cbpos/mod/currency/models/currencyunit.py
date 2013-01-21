import cbpos

import cbpos.mod.base.models.common as common

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

# TODO they are not used they should be assigned to an image of the coin or something and used to truncate to the nearest.
class CurrencyUnit(cbpos.database.Base, common.Item):
    __tablename__ = 'currency_units'

    id = Column(Integer, primary_key=True)
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    value = Column(Float, nullable=False)

    currency = relationship("Currency", order_by="Currency.id", backref="units")

    @hybrid_property
    def display(self):
        # TODO arrange the display property and expression of CurrencyUnit
        return '%s/%s' % (self.value, self.currency.symbol)
    
    @display.expression
    def display(self):
        return func.concat(self.value, '/', self.currency.symbol)

    def __lt__(self, other):
        if other.currency != self.currency:
            from cbpos.mod.currency.controllers import convert
            other_value = convert(other.value, other.currency, self.currency)
        else:
            other_value = other.value
        return self.value<other_value

    def __repr__(self):
        return "<CurrencyUnit %s>" % (self.currency.format(self.value),)