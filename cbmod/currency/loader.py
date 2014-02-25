from pydispatch import dispatcher

import cbpos
logger = cbpos.get_logger(__name__)

from cbpos.modules import BaseModuleLoader

class ModuleLoader(BaseModuleLoader):
    def load_models(self):
        from cbmod.currency.models import Currency, CurrencyUnit, CurrencyRate
        return [Currency, CurrencyUnit, CurrencyRate]

    def test_models(self):
        from cbmod.currency.models import Currency, CurrencyUnit, CurrencyRate
        
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
        from cbmod.currency.views import CurrenciesPage
        
        return [[],
                [MenuItem('currencies', parent='system',
                          label=cbpos.tr.currency_('Currencies'),
                          icon=cbpos.res.currency('images/menu-currencies.png'),
                          page=CurrenciesPage
                          )]
                ]
    
    def config_pages(self):
        from cbmod.currency.views import CurrencyConfigPage 
        return [CurrencyConfigPage]
    
    def first_run_wizard_pages(self):
        from cbmod.base.views.wizard import WizardPageCollection
        from cbmod.currency.views.wizard import CurrencySetupWizardPage
        
        class Wizards(WizardPageCollection):
            pages = (CurrencySetupWizardPage,)
        
        return Wizards()
