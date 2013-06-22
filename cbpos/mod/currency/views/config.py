from PySide import QtGui

import cbpos

import cbpos.mod.currency.controllers as currency
from cbpos.mod.currency.models.currency import Currency

class CurrencyConfigPage(QtGui.QWidget):
    label = 'Currency'
    
    def __init__(self):
        super(CurrencyConfigPage, self).__init__()
        
        self.default = QtGui.QComboBox()
        
        form = QtGui.QFormLayout()
        form.setSpacing(10)
        
        form.addRow('Default Currency', self.default)
        
        self.setLayout(form)

    def populate(self):
        session = cbpos.database.session()
        
        default_id = currency.default.id
        
        selected_index = -1
        self.default.clear()
        
        for i, c in enumerate(session.query(Currency)):
            self.default.addItem(c.display, c)
            if default_id == c.id:
                selected_index = i
        
        self.default.setCurrentIndex(selected_index)
    
    def update(self):
        default = self.default.itemData(self.default.currentIndex())
        cbpos.config['mod.currency', 'default'] = unicode(default.id)
