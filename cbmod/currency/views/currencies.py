from PySide import QtCore, QtGui

import cbpos

from cbmod.currency.controllers import CurrenciesFormController
from cbmod.currency.models import CurrencyRate 

from cbmod.base.views import FormPage

from babel.core import Locale
import sys

class CurrenciesPage(FormPage):
    controller = CurrenciesFormController()
    
    def widgets(self):
        
        currency_label = QtGui.QLabel(cbpos.tr.currency._("Currency value"))
        
        currency_value = QtGui.QDoubleSpinBox()
        currency_value.setRange(0, sys.maxint)
        currency_value.setSingleStep(1)
        
        reference_label = QtGui.QLabel(cbpos.tr.currency._("is equivalent to (reference)"))
        
        reference_value = QtGui.QDoubleSpinBox()
        reference_value.setRange(0, sys.maxint)
        reference_value.setSingleStep(1)
        
        rate = QtGui.QHBoxLayout()
        rate.addWidget(currency_label)
        rate.addWidget(currency_value)
        rate.addWidget(reference_label)
        rate.addWidget(reference_value)
        
        id_field = QtGui.QComboBox()
        for currency_id, currency_name in sorted(cbpos.locale.currencies.iteritems()):
            id_field.addItem(u'[{id}] {name}'.format(id=currency_id, name=currency_name), currency_id)
        
        return (("id", id_field),
                ("current_rate", rate)
                )
    
    def getDataFromControl(self, field):
        if field == 'id':
            selected = self.f[field].currentIndex()
            data = self.f[field].itemData(selected)
        elif field == 'current_rate':
            currency_value = self.f[field].itemAt(1).widget()
            reference_value = self.f[field].itemAt(3).widget()
            if self.item is not None:
                if self.item.current_rate.currency_value == currency_value.value() and \
                        self.item.current_rate.reference_value == reference_value.value():
                    data = None
                    field = None
            else:
                data = CurrencyRate(currency_value=currency_value.value(),
                                reference_value=reference_value.value())
        return (field, data)
    
    def setDataOnControl(self, field, data):
        if field == 'id':
            if data is not None:
                index = self.f[field].findData(data)
                self.f[field].setCurrentIndex(index)
            else:
                self.f[field].setCurrentIndex(-1)
            
            # Only enable changing the currency if it's a new one
            self.f[field].setEnabled(self.editing and self.item is None)
        elif field in 'current_rate':
            currency_value = self.f[field].itemAt(1).widget()
            reference_value = self.f[field].itemAt(3).widget()
            if data is not None:
                currency_value.setValue(data.currency_value)
                reference_value.setValue(data.reference_value)
            else:
                currency_value.setValue(0)
                reference_value.setValue(0)
