from django import forms 
from django.db.models import Q

from tempus_dominus.widgets import DatePicker
import os.path

from .models import (
    ChequingAccount, CreditCardAccount, ChequingTransaction, CreditCardTransaction,
    ExpenseType, Location, ExpenseRecord, Tag)

from base.widgets import RelatedFieldWidgetSingle, RelatedFieldWidgetMultiple



class ChequingAccountForm(forms.ModelForm):
  
    name = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            )
        )

    class Meta:
        model = ChequingAccount
        fields = ['name', 'notes' ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)


class CreditCardAccountForm(forms.ModelForm):
  
    name = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            )
        )

    class Meta:
        model = CreditCardAccount
        fields = ['name',  'notes' ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)


class ChequingTransactionForm(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(
        required=False, 
        queryset=Tag.objects.all(), 
        widget=RelatedFieldWidgetMultiple(
            Tag, 
            related_url="bankexp:tag_add",
            attrs={'class': 'select2-bankexp', 'style': 'width:90%'}, 
            )
        )

    tr_date = forms.DateTimeField(widget=DatePicker())

    account = forms.ModelChoiceField(
        required=True, 
        queryset=ChequingAccount.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            ChequingAccount, 
            related_url="bankexp:chequingaccount_add", 
            attrs={'class': 'select2-bankexp form-control', 'style': 'width:90%' },   
            )
        )

    tr_desc = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            )
        )

    class Meta:
        model = ChequingTransaction
        fields = [
            'account', 
            'tr_date', 
            'tr_desc', 
            'tr_withdrawal', 
            'tr_deposits', 
            'tr_balance', 
            'tags' 
            ]
        widgets = {
            'tr_withdrawal': forms.NumberInput(attrs={'class': 'select2-bankexp form-control' }),
            'tr_deposits': forms.NumberInput(attrs={'class': 'select2-bankexp form-control' }),
            'tr_balance': forms.NumberInput(attrs={'class': 'select2-bankexp form-control' }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = ChequingAccount.objects.filter(owner=self.user)
        self.fields['tags'].queryset = Tag.objects.filter(owner=self.user)
        

class CreditCardTransactionForm(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(
        required=False, 
        queryset=Tag.objects.all(), 
        widget=RelatedFieldWidgetMultiple(
            Tag, 
            related_url="bankexp:tag_add",
            attrs={'class': 'select2-bankexp', 'style': 'width:90%'}, 
            )
        )

    tr_date = forms.DateTimeField(widget=DatePicker( ))

    account = forms.ModelChoiceField(
        required=True, 
        queryset=CreditCardAccount.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            CreditCardAccount, 
            related_url="bankexp:creditcardaccount_add", 
            attrs={'class': 'select2-bankexp form-control', 'style': 'width:90%' },  
            )
        )

    tr_desc = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            )
        )

    class Meta:
        model = CreditCardTransaction
        fields = [
            'account', 
            'tr_date', 
            'tr_desc', 
            'tr_debit', 
            'tr_credit', 
            'tr_balance', 
            'tags' 
            ]
        widgets = {
            'tr_debit': forms.NumberInput(attrs={'class': 'select2-bankexp form-control' }),
            'tr_credit': forms.NumberInput(attrs={'class': 'select2-bankexp form-control' }),
            'tr_balance': forms.NumberInput(attrs={'class': 'select2-bankexp form-control' }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = CreditCardAccount.objects.filter(owner=self.user)
        self.fields['tags'].queryset = Tag.objects.filter(owner=self.user)
        

class ExpenseTypeForm(forms.ModelForm):
  
    name = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            )
        )

    class Meta:
        model = ExpenseType
        fields = ['name',  'notes', ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)


class LocationForm(forms.ModelForm):
  
    name = forms.CharField(
        required=True, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            )
        )

    address = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            )
        )

    prov_st = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            )
        )

    country = forms.CharField(
        required=False, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
            )
        )

    class Meta:
        model = Location
        fields = ['name', 'address', 'prov_st', 'country', 'notes']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)


class ChequingTransactionModelChoiceField(forms.ModelChoiceField):
    """
    Subclassing ModelChoiceField to change the display
    for the transaction. It shows transaction description and 
    transaction date.
    """
    def label_from_instance(self, obj):
        if obj.tr_withdrawal:
            return f"{obj.tr_desc} - {obj.tr_withdrawal} ({obj.tr_date})"
        else:
            return f"{obj.tr_desc} - {obj.tr_deposits} ({obj.tr_date})"


class CreditCardTransactionModelChoiceField(forms.ModelChoiceField):
    """
    Subclassing ModelChoiceField to change the display
    for the transaction. It shows transaction description and 
    transaction date.
    """
    def label_from_instance(self, obj):
        if obj.tr_debit:
            return f"{obj.tr_desc} - {obj.tr_debit} ({obj.tr_date})"
        else:
            return f"{obj.tr_desc} - {obj.tr_credit} ({obj.tr_date})"


class ExpenseRecordForm(forms.ModelForm):

    exp_date = forms.DateField(
        required=True, 
        widget=DatePicker(attrs={'class': 'form-control'}))

    exp_type = forms.ModelChoiceField(
        required=True, 
        queryset=ExpenseType.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            ExpenseType, 
            related_url="bankexp:expensetype_add", 
            attrs={'class': 'select2-bankexp form-control',
                   'style': 'width:90%'},  
            )
        )

    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=3,
        required = True,
        min_value = 0,
        initial = 0,
        widget = forms.NumberInput(
            attrs={'class': 'form-control', 'style': 'width:30%'}
            )
        )

    chq_tr = ChequingTransactionModelChoiceField(
        required=False, 
        queryset=ChequingTransaction.objects.all().prefetch_related('account'), 
        widget=RelatedFieldWidgetSingle(
            ChequingTransaction, 
            related_url="bankexp:chequingtransaction_add", 
            attrs={'class': 'select2-bankexp form-control',
                   'style': 'width:90%'},  
            )
        )

    cc_tr = CreditCardTransactionModelChoiceField(
        required=False, 
        queryset=CreditCardTransaction.objects.all().prefetch_related('account'), 
        widget=RelatedFieldWidgetSingle(
            CreditCardTransaction, 
            related_url="bankexp:creditcardtransaction_add", 
            attrs={'class': 'select2-bankexp form-control',
                   'style': 'width:90%'},  
            )
        )

    tax = forms.DecimalField(
        max_digits=10, 
        decimal_places=3,
        required = False,
        min_value = 0,
        initial = 0,
        widget = forms.NumberInput(
            attrs={'class': 'form-control', 'style': 'width:30%'}
            )
        )

    location = forms.ModelChoiceField(
        required=False, 
        queryset=Location.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Location, 
            related_url="bankexp:location_add", 
            attrs={'class': 'select2-bankexp form-control',
                   'style': 'width:90%'},  
            )
        )
    
    class Meta:
        model = ExpenseRecord
        fields = [
            'exp_type', 
            'exp_date', 
            'amount', 
            'tax', 
            'location', 
            'chq_tr', 
            'cc_tr',  
            'details', 
            'quantity', 
            'files', 
            ]
        widgets = {
          'quantity': forms.TextInput(attrs={'class': 'form-control',  'style': 'width:30%'}),
          'details': forms.Textarea(attrs={'class': 'form-control', 'style': 'border: none', }),
       }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields['exp_type'].queryset = ExpenseType.objects.filter(owner=self.user)
        self.fields['location'].queryset = Location.objects.filter(owner=self.user)
        self.fields['chq_tr'].queryset = ChequingTransaction.objects.filter(owner=self.user)
        self.fields['cc_tr'].queryset = CreditCardTransaction.objects.filter(owner=self.user)
        

class TagForm(forms.ModelForm):
  
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Tag
        fields = ['name', 'notes' ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        

class TagMultipleAssignForm(forms.Form):
    """ 
    Form used for assigning a tag to multiple 
    transactions in one step.
    """
    string_expr = forms.CharField(
        required=True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control form-tag-multiple', 'style': 'width:90%'}
        ))
    tag = forms.ModelChoiceField(
        required=True, 
        queryset=Tag.objects.all(), 
        widget=RelatedFieldWidgetSingle(
            Tag, 
            related_url="bankexp:tag_add", 
            attrs={'class': 'select2-bankexp form-tag-multiple',
                   'style': 'width:90%'},  
            )
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['tag'].queryset = Tag.objects.filter(owner=self.user)

    
class TagMultipleRemoveForm(forms.Form):
    """ 
    Form used for removing a tag from multiple 
    transactions in one step.
    """

    tag = forms.ModelChoiceField(
        required=True, 
        queryset=Tag.objects.all(), 
        widget=forms.Select( 
            attrs={'class': 'select2-bankexp form-control',
                   },  
            )
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['tag'].queryset = Tag.objects.filter(owner=self.user)


class ImportForm(forms.Form):

    import_file = forms.FileField(
        label='File to import'
        )
        
    input_format = forms.ChoiceField(
        label='Format',
        choices=(),
        widget=forms.Select(
            attrs={'class': 'select2-bankexp',}
            )
        )

    def __init__(self, import_formats, *args, **kwargs):

        super().__init__(*args, **kwargs)
        choices = []
        for i, f in enumerate(import_formats):
            choices.append((str(i), f().get_title(),))
        if len(import_formats) > 1:
            choices.insert(0, ('', '---'))

        self.fields['input_format'].choices = choices


class ConfirmImportForm(forms.Form):
    import_file_name = forms.CharField(widget=forms.HiddenInput())
    original_file_name = forms.CharField(widget=forms.HiddenInput())
    input_format = forms.CharField(widget=forms.HiddenInput())

    def clean_import_file_name(self):
        data = self.cleaned_data['import_file_name']
        data = os.path.basename(data)
        return data


class ExportForm(forms.Form):

    file_format = forms.ChoiceField(
        label='File Format',
        choices=(),
        widget=forms.Select(
            attrs={'class': 'select2-bankexp',}
            )
        )

    def __init__(self, formats, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        for i, f in enumerate(formats):
            choices.append((str(i), f().get_title(),))
        if len(formats) > 1:
            choices.insert(0, ('', '---'))

        self.fields['file_format'].choices = choices


class DateRangeForm(forms.Form):
    date_from = forms.DateField(required=True, widget=DatePicker())
    date_to = forms.DateField(required=True, widget=DatePicker())