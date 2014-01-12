from PySide import QtGui

import cbpos

logger = cbpos.get_logger(__name__)

from cbmod.currency.models import Currency

from cbmod.currency.views import CurrenciesPage

class CurrencyDialog(QtGui.QWidget):
    
    def __init__(self):
        super(CurrencyDialog, self).__init__()

        message = cbpos.tr.currency._("Set up the currencies you will be using. You will be able to change them later also.")

        self.message = QtGui.QLabel(message)

        self.form = CurrenciesPage()
        
        buttonBox = QtGui.QDialogButtonBox()
        
        self.doneBtn = buttonBox.addButton(QtGui.QDialogButtonBox.Close)
        self.doneBtn.pressed.connect(self.onDoneButton)
        
        layout = QtGui.QVBoxLayout()
        layout.setSpacing(10)

        layout.addWidget(self.message)        
        layout.addWidget(self.form)
        layout.addWidget(buttonBox)
        
        self.setLayout(layout)
    
    def onDoneButton(self):
        session = cbpos.database.session()
        currency = session.query(Currency).first()
        
        if currency is None:
            QtGui.QMessageBox.warning(self, cbpos.tr.currency._("No currency"),
                                            cbpos.tr.currency._("You have to sest up at least one currency"),
                                            QtGui.QMessageBox.Ok)
            return
        
        cbpos.config["mod.currency", "default"] = currency.id
        self.close()
        
        cbpos.ui.show_next()
