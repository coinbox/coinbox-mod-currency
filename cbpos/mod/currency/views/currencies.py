from PySide import QtCore, QtGui

import cbpos

from cbpos.mod.currency.controllers import CurrenciesFormController
from cbpos.mod.currency.models.currency import Currency

from cbpos.mod.base.views import FormPage

class CurrenciesPage(FormPage):
    controller = CurrenciesFormController()
    
    def widgets(self):
        value = QtGui.QDoubleSpinBox()
        value.setMinimum(0)
        value.setSingleStep(1)
        
        decimalPlaces = QtGui.QSpinBox()
        decimalPlaces.setRange(0, 10)
        decimalPlaces.setSingleStep(1)
        
        return (("name", QtGui.QLineEdit()),
                ("symbol", QtGui.QLineEdit()),
                ("value", value),
                ("decimal_places", decimalPlaces),
                ("digit_grouping", QtGui.QCheckBox()),
                )
    
    def getDataFromControl(self, field):
        if field in ('name', 'symbol'):
            data = self.f[field].text()
        elif field in ('value', 'decimal_places'):
            data = self.f[field].value()
        elif field == 'digit_grouping':
            data = self.f[field].isChecked()
        return (field, data)
    
    def setDataOnControl(self, field, data):
        if field in ('name', 'symbol'):
            self.f[field].setText(data)
        elif field in ('value', 'decimal_places'):
            self.f[field].setValue(data)
        elif field == 'digit_grouping':
            self.f[field].setChecked(data)
