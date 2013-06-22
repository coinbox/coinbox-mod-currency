from pydispatch import dispatcher

import cbpos
from cbpos.modules import BaseModuleLoader

class ModuleLoader(BaseModuleLoader):
    dependencies = ('base',)
    name = 'Multiple Currencies Support'

    def load(self):
        from cbpos.mod.currency.models import Currency, CurrencyUnit, CurrencyRate
        return [Currency, CurrencyUnit, CurrencyRate]

    def test(self):
        from cbpos.mod.currency.models import Currency, CurrencyUnit, CurrencyRate
        
        LBP = Currency(id='LBP')
        USD = Currency(id='USD')
        EUR = Currency(id='EUR')
        
        # Taking .01 USD (1 cent) as a reference
        
        LBP.current_rate = CurrencyRate(currency_value=1500, reference_value=100)
        USD.current_rate = CurrencyRate(currency_value=1, reference_value=100)
        EUR.current_rate = CurrencyRate(currency_value=1, reference_value=129)
        
        lbp_values = [250, 500, 1000, 5000, 10000, 20000, 50000, 100000]
        usd_values = [0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1, 2, 5, 10, 20, 50, 100]
        eur_values = [0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1, 2, 5, 10, 20, 50, 100, 500]
    
        [CurrencyUnit(value=v, currency=LBP) for v in lbp_values]
        [CurrencyUnit(value=v, currency=USD) for v in usd_values]
        [CurrencyUnit(value=v, currency=EUR) for v in eur_values]
    
        session = cbpos.database.session()
        session.add(LBP)
        session.add(USD)
        session.add(EUR)
        session.commit()

    def menu(self):
        from cbpos.interface import MenuItem
        from cbpos.mod.currency.views import CurrenciesPage
        
        return [[],
                [MenuItem('currencies', parent='system',
                          label=cbpos.tr.currency._('Currencies'),
                          icon=cbpos.res.currency('images/menu-currencies.png'),
                          page=CurrenciesPage
                          )]
                ]

    def init(self):
        from cbpos.mod.currency.models import Currency
        
        session = cbpos.database.session()
        currency_count = session.query(Currency).count()
        if currency_count == 0:
            dispatcher.connect(self.do_prompt_currency, signal='ui-post-init', sender='app')
        
        return True
    
    def do_prompt_currency(self):
        from cbpos.mod.currency.views.dialogs import CurrencyDialog
        
        win = CurrencyDialog()
        cbpos.ui.window = win
        cbpos.break_init()
        cbpos.load_database(True)
    
    def config_pages(self):
        from cbpos.mod.currency.views import CurrencyConfigPage 
        return [CurrencyConfigPage]
