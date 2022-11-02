from django.contrib.auth.models import User

from import_export import resources, widgets, fields

from .models import (
    ChequingAccount, CreditCardAccount, ChequingTransaction, CreditCardTransaction,
    ExpenseType, Location, ExpenseRecord, Tag)




class TransactionAccountForeignKeyWidget(widgets.ForeignKeyWidget):
        def get_queryset(self, value, row, *args, **kwargs):           
            return self.model.objects.filter( owner__username=row["owner"], )


class ChequingAccountResource(resources.ModelResource):
    name = fields.Field(
        column_name='name', 
        attribute='name', 
        widget=widgets.CharWidget())

    owner = fields.Field(
        column_name='owner', 
        attribute='owner', 
        widget=widgets.ForeignKeyWidget(User, field='username'),
        saves_null_values=False)

    notes = fields.Field(
        column_name='notes', 
        attribute='notes', 
        widget=widgets.CharWidget())

    
    class Meta:
        model = ChequingAccount
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('owner', )
        fields = ('name', 'owner', 'notes', )


class CreditCardAccountResource(resources.ModelResource):

    name = fields.Field(
        column_name='name', 
        attribute='name', 
        widget=widgets.CharWidget())

    owner = fields.Field(
        column_name='owner', 
        attribute='owner', 
        widget=widgets.ForeignKeyWidget(User, field='username'),
        saves_null_values=False)

    notes = fields.Field(
        column_name='notes', 
        attribute='notes', 
        widget=widgets.CharWidget())
   

    class Meta:
        model = CreditCardAccount
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('owner', )
        fields = ('name', 'owner', 'notes', )


class ChequingTransactionResource(resources.ModelResource):

    account = fields.Field(
        column_name='account', 
        attribute='account', 
        widget=TransactionAccountForeignKeyWidget(ChequingAccount, 'name'),
        saves_null_values=False) 

    owner = fields.Field(
        column_name='owner', 
        attribute='owner', 
        widget=widgets.ForeignKeyWidget(User, field='username'),
        saves_null_values=False)

    tags = fields.Field(
        column_name='tags', 
        attribute='tags', 
        widget=widgets.ManyToManyWidget(Tag, field='name'))


    class Meta:
        model = ChequingTransaction
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('account', 'tr_date', 'tr_desc', 'tr_withdrawal', 'tr_deposits', 'tr_balance', 'owner')
        fields = ('account', 'tr_date', 'tr_desc', 'tr_withdrawal', 'tr_deposits', 'tr_balance', 'owner')

    
class CreditCardTransactionResource(resources.ModelResource):

    account = fields.Field(
        column_name='account', 
        attribute='account', 
        widget=TransactionAccountForeignKeyWidget(CreditCardAccount, 'name'),
        saves_null_values=False) 

    owner = fields.Field(
        column_name='owner', 
        attribute='owner', 
        widget=widgets.ForeignKeyWidget(User, field='username'),
        saves_null_values=False)

    tags = fields.Field(
        column_name='tags', 
        attribute='tags', 
        widget=widgets.ManyToManyWidget(Tag, field='name'))

    class Meta:
        model = CreditCardTransaction
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('account', 'tr_date', 'tr_desc', 'tr_debit', 'tr_credit', 'tr_balance', 'owner')
        fields = ('account', 'tr_date', 'tr_desc', 'tr_debit', 'tr_credit', 'tr_balance', 'owner')


class ExpenseTypeResource(resources.ModelResource):

    name = fields.Field(
        column_name='name', 
        attribute='name', 
        widget=widgets.CharWidget())

    owner = fields.Field(
        column_name='owner', 
        attribute='owner', 
        widget=widgets.ForeignKeyWidget(User, field='username'),
        saves_null_values=False)
   

    class Meta:
        model = ExpenseType
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('owner', )
        fields = ('name', 'owner', 'notes')


class LocationResource(resources.ModelResource):

    name = fields.Field(
        column_name='name', 
        attribute='name', 
        widget=widgets.CharWidget())

    address = fields.Field(
        column_name='address', 
        attribute='address', 
        widget=widgets.CharWidget())

    prov_st = fields.Field(
        column_name='prov_st', 
        attribute='prov_st', 
        widget=widgets.CharWidget())

    country = fields.Field(
        column_name='country', 
        attribute='country', 
        widget=widgets.CharWidget())

    owner = fields.Field(
        column_name='owner', 
        attribute='owner', 
        widget=widgets.ForeignKeyWidget(User, field='username'),
        saves_null_values=False)
   

    class Meta:
        model = Location
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('owner',  )
        fields = ('name', 'address', 'prov_st', 'country', 'owner',  )


class ExpenseRecordResource(resources.ModelResource):

    exp_type = fields.Field(
        column_name='exp_type', 
        attribute='exp_type', 
        widget=widgets.ForeignKeyWidget(ExpenseType, 'name'),
        saves_null_values=False) 

    owner = fields.Field(
        column_name='owner', 
        attribute='owner', 
        widget=widgets.ForeignKeyWidget(User, field='username'),
        saves_null_values=False)

    chq_tr = fields.Field(
        column_name='chq_tr', 
        attribute='chq_tr', 
        widget=widgets.ForeignKeyWidget(ChequingTransaction, 'tr_desc'),
        saves_null_values=True) 

    cc_tr = fields.Field(
        column_name='cc_tr', 
        attribute='cc_tr', 
        widget=widgets.ForeignKeyWidget(CreditCardTransaction, 'tr_desc'),
        saves_null_values=True) 

    location = fields.Field(
        column_name='location', 
        attribute='location', 
        widget=widgets.ForeignKeyWidget(Location, 'name'),
        saves_null_values=True)

    exp_date = fields.Field(
        attribute='exp_date', 
        column_name='exp_date', 
        widget=widgets.DateWidget('%Y-%m-%d')) 

    amount = fields.Field(
        column_name='amount', 
        attribute='amount', 
        widget=widgets.DecimalWidget())

    quantity = fields.Field(
        column_name='quantity', 
        attribute='quantity', 
        widget=widgets.CharWidget())

    details = fields.Field(
        column_name='details', 
        attribute='details', 
        widget=widgets.CharWidget())


    class Meta:
        model = ExpenseRecord
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = (
            'owner',
            'exp_type', 
            'exp_date', 
            'amount', 
            'location', 
            'chq_tr', 
            'cc_tr', 
            'quantity', 
            )
        fields = (
            'exp_type', 
            'exp_date', 
            'amount', 
            'location', 
            'chq_tr', 
            'cc_tr', 
            'quantity', 
            'details',
            'owner')


class TagResource(resources.ModelResource):

    name = fields.Field(
        column_name='name', 
        attribute='name', 
        widget=widgets.CharWidget())

    owner = fields.Field(
        column_name='owner', 
        attribute='owner', 
        widget=widgets.ForeignKeyWidget(User, field='username'),
        saves_null_values=False)
   

    class Meta:
        model = Tag
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ('owner', 'name' )
        fields = ('name', 'owner',  )

