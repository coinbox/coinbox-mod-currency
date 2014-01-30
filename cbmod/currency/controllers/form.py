import cbpos

from cbmod.currency.models import Currency, CurrencyUnit

from cbmod.base.controllers import FormController

class CurrenciesFormController(FormController):
    cls = Currency
    
    def fields(self):
        return {"id": (cbpos.tr.currency_("Currency"), None),
                "current_rate": (cbpos.tr.currency_("Currency Rate"), None)
                }
    
    def items(self):
        session = cbpos.database.session()
        return session.query(Currency)
    
    def canDeleteItem(self, item):
        return True
    
    def canEditItem(self, item):
        return True
    
    def canAddItem(self):
        return True
    
    def getDataFromItem(self, field, item):
        return getattr(item, field)
