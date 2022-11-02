from django.contrib import admin
from django.contrib.auth.models import User
from django import forms

from import_export.admin import ImportExportModelAdmin
from import_export.forms import ConfirmImportForm, ImportForm

from .models import (
    ChequingAccount, CreditCardAccount, ChequingTransaction, CreditCardTransaction,
    ExpenseType, Location, ExpenseRecord, Tag)

from .resources import (
    ChequingAccountResource, CreditCardAccountResource, ChequingTransactionResource, 
    CreditCardTransactionResource, ExpenseTypeResource, LocationResource, 
    ExpenseRecordResource, TagResource)




class ChequingAccountAdmin(ImportExportModelAdmin):
    exclude = ('owner',)
    list_display = ('name', 'owner')
    search_fields = ('name',)
    resource_class = ChequingAccountResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
        
    def save_model(self, request, obj, form, change):
        obj.owner = request.user                
        obj.save()


class CreditCardAccountAdmin(ImportExportModelAdmin):
    exclude = ('owner',)
    list_display = ('name',  'owner')
    search_fields = ('name',)
    resource_class = CreditCardAccountResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
        
    def save_model(self, request, obj, form, change):
        obj.owner = request.user                
        obj.save()


class CustomImportForm(ImportForm):
   owner = forms.ModelChoiceField(
       queryset=User.objects.all(),
       required=True)

class CustomConfirmImportForm(ConfirmImportForm):
   owner = forms.ModelChoiceField(
       queryset=User.objects.all(),
       required=True)


class ChequingTransactionAdmin(ImportExportModelAdmin):
    exclude = ('owner',)
    list_display = (
        '__str__', 
        "account", 
        'tr_date', 
        'tr_desc', 
        'tr_withdrawal', 
        'tr_deposits', 
        'tr_balance', 
        'owner'
        )
    search_fields = ('tr_desc',)
    resource_class = ChequingTransactionResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
        
    def save_model(self, request, obj, form, change):
        obj.owner = request.user                
        obj.save()


class CustomChequingTransactionAdmin(ChequingTransactionAdmin):
    """BookAdmin with custom import forms"""

    def get_import_form(self):
        return CustomImportForm

    def get_confirm_import_form(self):
        return CustomConfirmImportForm

    def get_form_kwargs(self, form, *args, **kwargs):
        if isinstance(form, CustomImportForm):
            if form.is_valid():
                owner = form.cleaned_data['owner']
                kwargs.update({'owner': owner.id})
        return kwargs


class CreditCardTransactionAdmin(ImportExportModelAdmin):
    exclude = ('owner',)
    list_display = (
        '__str__', 
        'account', 
        'tr_date', 
        'tr_desc', 
        'tr_debit', 
        'tr_credit', 
        'tr_balance', 
        'owner'
        )
    search_fields = ('tr_desc',)
    resource_class = CreditCardTransactionResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
        
    def save_model(self, request, obj, form, change):
        obj.owner = request.user                
        obj.save()


class ExpenseTypeAdmin(ImportExportModelAdmin):
    exclude = ('owner',)
    list_display = ('name', )
    search_fields = ('name',)
    resource_class = ExpenseTypeResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
        
    def save_model(self, request, obj, form, change):
        obj.owner = request.user                
        obj.save()


class LocationAdmin(ImportExportModelAdmin):
    exclude = ('owner',)
    list_display = ('name', )
    search_fields = ('name',)
    resource_class = LocationResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
        
    def save_model(self, request, obj, form, change):
        obj.owner = request.user                
        obj.save()


class ExpenseRecordAdmin(ImportExportModelAdmin):
    exclude = ('owner',)
    list_display = ( 
        '__str__', 
        'exp_type', 
        'exp_date',  
        'amount', 
        'tax', 
        'location', 
        'chq_tr', 
        'cc_tr', 
        'quantity'
        )
    search_fields = ('tr_desc', 'location')
    resource_class = ExpenseRecordResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
        
    def save_model(self, request, obj, form, change):
        obj.owner = request.user                
        obj.save()


class TagAdmin(ImportExportModelAdmin):
    exclude = ('owner',)
    list_display = ('name', )
    search_fields = ('name',)
    resource_class = TagResource

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
        
    def save_model(self, request, obj, form, change):
        obj.owner = request.user                
        obj.save()




admin.site.register(ChequingAccount, ChequingAccountAdmin)
admin.site.register(CreditCardAccount, CreditCardAccountAdmin)
admin.site.register(ChequingTransaction, ChequingTransactionAdmin)
admin.site.register(CreditCardTransaction, CreditCardTransactionAdmin)
admin.site.register(ExpenseType, ExpenseTypeAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(ExpenseRecord, ExpenseRecordAdmin)
admin.site.register(Tag, TagAdmin)


