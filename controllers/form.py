import cbpos

from cbpos.mod.currency.models import Currency, CurrencyUnit

from cbpos.mod.base.controllers import FormController

class CurrenciesFormController(FormController):
    cls = Currency
    
    def fields(self):
        return {"name": (cbpos.tr.currency._("Name"), ""),
                "symbol": (cbpos.tr.currency._("Symbol"), ""),
                "value": (cbpos.tr.currency._("Value"), 0),
                "decimal_places": (cbpos.tr.currency._("Decimal Places"), 0),
                "digit_grouping": (cbpos.tr.currency._("Group Digits"), True)
                }
    
    def items(self):
        session = cbpos.database.session()
        items = session.query(Currency.display, Currency).all()
        return items
    
    def canDeleteItem(self, item):
        return True
    
    def canEditItem(self, item):
        return True
    
    def canAddItem(self):
        return True
    
    def getDataFromItem(self, field, item):
        return getattr(item, field)
