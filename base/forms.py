from django import forms



class BootstrapMixin(forms.BaseForm):
    """
    Add the base Bootstrap CSS classes to form elements.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        exempt_widgets = [
            forms.CheckboxInput,
            forms.ClearableFileInput,
            forms.FileInput,
            forms.RadioSelect
        ]

        for field_name, field in self.fields.items():
            if field.widget.__class__ not in exempt_widgets:
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = ' '.join([css, 'form-control']).strip()
            if field.required and not isinstance(field.widget, forms.FileInput):
                field.widget.attrs['required'] = 'required'
            if 'placeholder' not in field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label



OBJ_TYPE_CHOICES = (
    ('', 'All Objects'),
    ('BankExp', (
        ('chequingaccount', 'Chequing Accounts'),
        ('creditcardaccount', 'Credit Card Accounts'),
        ('chequingtransaction', 'Chequing Transactions'),
        ('creditcardtransaction', 'Credit Card Transactions'),
        ('expensetype', 'Expense Types'),
        ('expenserecord', 'Expense records'),
        ('tag', 'Tags'),
        ('location', 'Locations'),
    )),
)

class SearchForm(BootstrapMixin, forms.Form):
    q = forms.CharField(label='Search')
    obj_type = forms.ChoiceField(choices=OBJ_TYPE_CHOICES, required=False, label='Type')

