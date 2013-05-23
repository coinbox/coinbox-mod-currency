from PySide import QtGui

import cbpos

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
        currencies = session.query(Currency.name, Currency).all()
        default_id = cbpos.config['mod.currency', 'default']
        try:
            default_id = int(default_id)
        except ValueError:
            default_id = None
        
        self.default.clear()
        for i, c in enumerate(currencies):
            self.default.addItem(c[0], c[1])
            if default_id == c[1].id:
                self.default.setCurrentIndex(i)
    
    def update(self):
        default = self.default.itemData(self.default.currentIndex())
        cbpos.config['mod.currency', 'default'] = unicode(default.id)
