import django_tables2 as tables

from base.tables import BaseTable

from .models import (
    ChequingAccount, CreditCardAccount, ChequingTransaction, CreditCardTransaction,
    ExpenseType, Location, ExpenseRecord, Tag)




class ChequingAccountTable(BaseTable):

    name = tables.LinkColumn()
    
    class Meta(BaseTable.Meta):
        model = ChequingAccount       
        fields = ['name', ]
        attrs = {
                    'class': 'table table-sm',
                }

class CreditCardAccountTable(BaseTable):

    name = tables.LinkColumn()
    
    class Meta(BaseTable.Meta):
        model = CreditCardAccount       
        fields = ['name', ]
        attrs = {
                    'class': 'table table-sm',
                }

TR_LINK = """
<a href="{{ record.get_absolute_url }}">{{ record }}</a>
"""

class ChequingTransactionTable(BaseTable):

    account = tables.LinkColumn()
    tr_desc = tables.TemplateColumn(TR_LINK, verbose_name='Transaction')
    
    class Meta(BaseTable.Meta):
        model = ChequingTransaction      
        fields = ['tr_desc', 'account', 'tr_date', 'tr_withdrawal', 'tr_deposits', 'tr_balance',]
        attrs = {
                    'class': 'table table-sm',
                }


class CreditCardTransactionTable(BaseTable):

    account = tables.LinkColumn()
    tr_desc = tables.TemplateColumn(TR_LINK, verbose_name='Transaction')

    def transaction(self, value, record):
        return record
    
    class Meta(BaseTable.Meta):
        model = CreditCardTransaction       
        fields = [ 'tr_desc', 'account', 'tr_date', 'tr_debit', 'tr_credit', 'tr_balance',]
        attrs = {
                    'class': 'table table-sm',
                }


class ExpenseTypeTable(BaseTable):

    name = tables.LinkColumn()
    
    class Meta(BaseTable.Meta):
        model = ExpenseType       
        fields = ['name', ]
        attrs = {
                    'class': 'table table-sm',
                }

class LocationTable(BaseTable):

    name = tables.LinkColumn()
    
    class Meta(BaseTable.Meta):
        model = Location       
        fields = ['name', 'address', 'prov_st', 'country']
        attrs = {
                    'class': 'table table-sm',
                }

class ExpenseRecordTable(BaseTable):

    exp_type = tables.LinkColumn()
    
    class Meta(BaseTable.Meta):
        model = ExpenseRecord      
        fields = ['exp_type', 'exp_date', 'amount', 'location', 'quantity', ]
        attrs = {
                    'class': 'table table-sm',
                }


class TagTable(BaseTable):

    name = tables.LinkColumn()
    
    class Meta(BaseTable.Meta):
        model = Tag       
        fields = ['name', ]
        attrs = {
                    'class': 'table table-sm',
                }