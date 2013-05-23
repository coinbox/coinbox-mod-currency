import cbpos

from cbpos.mod.currency.models import Currency, CurrencyUnit

from cbpos.mod.base.controllers import FormController

class CurrenciesFormController(FormController):
    cls = Currency
    
    def fields(self):
        return {"id": (cbpos.tr.currency._("Currency"), None),
                "current_rate": (cbpos.tr.currency._("Currency Rate"), None)
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
