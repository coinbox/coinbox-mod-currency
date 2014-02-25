from PySide import QtGui

import cbpos

logger = cbpos.get_logger(__name__)

from cbmod.currency.models import Currency

from cbmod.currency.views import CurrenciesPage

from cbmod.base.views.wizard import BaseWizardPage

class CurrencySetupWizardPage(BaseWizardPage):
    def __init__(self, parent=None):
        super(CurrencySetupWizardPage, self).__init__(parent)
        
        message = cbpos.tr.currency_("Set up the currencies you will be using. You will be able to change them later also.")

        self.message = QtGui.QLabel(message)

        self.form = CurrenciesPage()
        
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(10)

        layout.addWidget(self.message)        
        layout.addWidget(self.form)
        
        self.setLayout(layout)
    
    def initializePage(self):
        self.form.populate()
    
    def validatePage(self):
        session = cbpos.database.session()
        currency = session.query(Currency).first()
        
        if currency is None:
            QtGui.QMessageBox.warning(self, cbpos.tr.currency_("No currency"),
                                            cbpos.tr.currency_("You have to set up at least one currency"),
                                            QtGui.QMessageBox.Ok)
            return False
        
        cbpos.config["mod.currency", "default"] = currency.id
        cbpos.config.save()
        return True
