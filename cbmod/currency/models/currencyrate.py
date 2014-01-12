import cbpos

import cbmod.base.models.common as common

from sqlalchemy import func, Table, Column, Integer, Numeric, String, Float, DateTime, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

from cbmod.currency.models.currency import CurrencyValue

class CurrencyRate(cbpos.database.Base, common.Item):
    __tablename__ = 'currency_rates'

    id = Column(Integer, primary_key=True)
    currency_id = Column(String(3), ForeignKey('currencies.id'), nullable=False)
    currency_value = Column(CurrencyValue(), nullable=False)
    reference_value = Column(CurrencyValue(), nullable=False)
    update_date = Column(DateTime, nullable=False, default=func.current_timestamp())

    currency = relationship("Currency",
                backref=backref("rates", lazy='dynamic',
                                order_by="desc(CurrencyRate.update_date)")
                            )
    
    @hybrid_property
    def reference_to_currency_ratio(self):
        return self.reference_value/self.currency_value
    
    @hybrid_property
    def currency_to_reference_ratio(self):
        return self.currency_value/self.reference_value
    
    def __repr__(self):
        return "<CurrencyRate %s %s:%s>" % (self.currency.id, self.currency_value, self.reference_value)
