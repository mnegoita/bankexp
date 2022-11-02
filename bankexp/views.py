from django.shortcuts import render
from django.views.generic import View, DetailView, ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy

from import_export.formats import base_formats
from datetime import date, timedelta

from .models import (
    ChequingAccount, CreditCardAccount, ChequingTransaction, CreditCardTransaction,
    ExpenseType, Location, ExpenseRecord, Tag)
from .filters import (ChequingAccountFilter, CreditCardAccountFilter, ChequingTransactionFilter, 
    CreditCardTransactionFilter, ExpenseTypeFilter, ExpenseRecordFilter, LocationFilter, TagFilter)
from .forms import (ChequingAccountForm, CreditCardAccountForm, ChequingTransactionForm, CreditCardTransactionForm, 
    ExpenseTypeForm, ExpenseRecordForm, LocationForm, TagForm, TagMultipleAssignForm, TagMultipleRemoveForm,
    DateRangeForm)
from .tables import (ChequingAccountTable, CreditCardAccountTable, ChequingTransactionTable, CreditCardTransactionTable, 
    ExpenseTypeTable, ExpenseRecordTable, LocationTable, TagTable)
from .resources import (ChequingAccountResource, CreditCardAccountResource, ChequingTransactionResource, CreditCardTransactionResource,  
    ExpenseRecordResource, ExpenseTypeResource, LocationResource, TagResource)
from .import_export_views import TransactionImportView, ImportView, ExportView


from base.views import (
    BaseItemsList, BaseItemsSearchresults, BaseItemCreateWithPopup, BaseItemCreate,
    BaseItemEdit, BaseItemDelete)

template_path = 'bankexp/'




# Chequing Account Views #################################################

class ChequingAccountList(BaseItemsList):
    model = ChequingAccount


class ChequingAccountSearchResults(BaseItemsSearchresults):
    queryset = ChequingAccount.objects.all()
    table = ChequingAccountTable
    filter = ChequingAccountFilter


class ChequingAccountDetail(SingleObjectMixin, View):
    template_name = template_path + "chq_acc_detail.html"
    queryset = ChequingAccount.objects.all()

    def get(self, request, *args, **kwargs):
       
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        current_date = date.today()
        date_from = current_date + timedelta(-180)
        date_to = current_date
        
        chq_trs = ChequingTransaction.objects.filter(
            owner=self.request.user, 
            account=self.object, 
            tr_date__gte=date_from, 
            tr_date__lte=date_to
            ).prefetch_related('account', 'tags') 

        form = DateRangeForm()
      
        context['form'] = form
        context['date_from'] = date_from
        context['date_to'] = date_to
        context['chq_trs'] = chq_trs

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form = DateRangeForm(request.POST)
        
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['form'] = form

        if form.is_valid():

            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

            chq_trs = ChequingTransaction.objects.filter(
                owner=self.request.user, 
                account=self.object, 
                tr_date__gte=date_from, 
                tr_date__lte=date_to
                ).prefetch_related('account', 'tags') 

            form = DateRangeForm()

            context['date_from'] = date_from
            context['date_to'] = date_to
            context['chq_trs'] = chq_trs

            return render(request, self.template_name, context)         

        return render(request, self.template_name, context)   


class ChequingAccountCreate(BaseItemCreateWithPopup):
    model = ChequingAccount
    form_class = ChequingAccountForm
    template_name = template_path + "chq_acc_form.html"
    template_name_popup = template_path + "chq_acc_form_popup.html"
    cancel_button_url = reverse_lazy('bankexp:chequingaccount_list')


class ChequingAccountEdit(BaseItemEdit):
    model = ChequingAccount
    form_class = ChequingAccountForm
    template_name = template_path + "chq_acc_form.html"


class ChequingAccountDelete(BaseItemDelete):
    model = ChequingAccount
    template_name = template_path + "chq_acc_confirm_delete.html"
    success_url = reverse_lazy('bankexp:chequingaccount_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chq_trs = self.object.transactions.all()
        chq_trs_count = self.object.transactions.all().count()
        context['chq_trs'] = chq_trs
        context['chq_trs_count'] = chq_trs_count
        return context


class ChequingAccountImport(ImportView):
    model = ChequingAccount
    resource_class = ChequingAccountResource
    template_name = template_path + "chq_acc_import.html"
    success_url = reverse_lazy('bankexp:chequingaccount_list')
    formats = (base_formats.CSV, base_formats.XLS,)

    
    def get_queryset(self):
        return ChequingAccount.objects.filter(owner=self.request.user)
        
    def create_dataset(self, *args, **kwargs):
        """ 
        Insert owner and account fields into the data.
        """  

        dataset = super().create_dataset(*args, **kwargs)
        length = len(dataset._data)
        dataset.append_col([self.request.user.username] * length,
                           header="owner")   

        return dataset

class ChequingAccountExport(ExportView):
    resource_class = ChequingAccountResource
    model = ChequingAccount
    template_name = template_path + "chq_acc_export.html"
    formats = (base_formats.CSV, base_formats.XLS,)

    def get_queryset(self):
        return ChequingAccount.objects.filter(owner=self.request.user)


# Credit Card Account Views ###########################################

class CreditCardAccountList(BaseItemsList):
    model = CreditCardAccount


class CreditCardAccountSearchResults(BaseItemsSearchresults):
    queryset = CreditCardAccount.objects.all()
    table = CreditCardAccountTable
    filter = CreditCardAccountFilter    


class CreditCardAccountDetail(SingleObjectMixin, View):
    template_name = template_path + "cc_acc_detail.html"
    queryset = CreditCardAccount.objects.all()

    def get(self, request, *args, **kwargs):
       
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        current_date = date.today()
        date_from = current_date + timedelta(-180)
        date_to = current_date
        
        cc_trs = CreditCardTransaction.objects.filter(
            owner=self.request.user, 
            account=self.object, 
            tr_date__gte=date_from, 
            tr_date__lte=date_to
            ).prefetch_related('account', 'tags') 

        form = DateRangeForm()
      
        context['form'] = form
        context['date_from'] = date_from
        context['date_to'] = date_to
        context['cc_trs'] = cc_trs

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        form = DateRangeForm(request.POST)
        
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['form'] = form

        if form.is_valid():

            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

            cc_trs = CreditCardTransaction.objects.filter(
                owner=self.request.user, 
                account=self.object, 
                tr_date__gte=date_from, 
                tr_date__lte=date_to
                ).prefetch_related('account', 'tags') 

            form = DateRangeForm()

            context['date_from'] = date_from
            context['date_to'] = date_to
            context['cc_trs'] = cc_trs

            return render(request, self.template_name, context)         

        return render(request, self.template_name, context)  


class CreditCardAccountCreate(BaseItemCreateWithPopup):
    model = CreditCardAccount
    form_class = CreditCardAccountForm
    template_name = template_path + "cc_acc_form.html"
    template_name_popup = template_path + "cc_acc_form_popup.html"
    cancel_button_url = reverse_lazy('bankexp:creditcardaccount_list')


class CreditCardAccountEdit(BaseItemEdit):
    model = CreditCardAccount
    form_class = CreditCardAccountForm
    template_name = template_path + "cc_acc_form.html"


class CreditCardAccountDelete(BaseItemDelete):
    model = CreditCardAccount
    template_name = template_path + "cc_acc_confirm_delete.html"
    success_url = reverse_lazy('bankexp:creditcardaccount_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cc_trs_count = self.object.transactions.all().count()
        context['cc_trs_count'] = cc_trs_count
        return context


class CreditCardAccountImport(ImportView):
    model = CreditCardAccount
    resource_class = CreditCardAccountResource
    template_name = template_path + "cc_acc_import.html"
    success_url = reverse_lazy('bankexp:creditcardaccount_list')
    formats = (base_formats.CSV, base_formats.XLS,)

    
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)
        
    def create_dataset(self, *args, **kwargs):
        """ 
        Insert owner and account fields into the data.
        """  

        dataset = super().create_dataset(*args, **kwargs)
        length = len(dataset._data)
        dataset.append_col([self.request.user.username] * length,
                           header="owner")   

        return dataset
    

class CreditCardAccountExport(ExportView):
    model = CreditCardAccount
    resource_class = CreditCardAccountResource
    template_name = template_path + "cc_acc_export.html"
    formats = (base_formats.CSV, base_formats.XLS,)

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


# Chequing Transaction Views #############################################

class ChequingTransactionTableView(View):
    """
    A class to display the chequing transactions (using DataTables)
    It still uses the url for list even that the template displays 
    the table with transactions.
    """

    template_name = template_path + "chq_tr_table.html"
    model = ChequingTransaction
    queryset = ChequingTransaction.objects.all().prefetch_related('account', 'tags',)

    def get(self, request):

        current_date = date.today()
        date_from = current_date + timedelta(-180)
        date_to = current_date
        self.queryset = self.queryset.filter(owner=request.user, tr_date__gte=date_from, tr_date__lte=date_to )

        form = DateRangeForm()
        
        obj_name = self.model._meta.verbose_name.lower().replace(" ", "")
        app_name = self.model._meta.app_label
        model = self.model

        return render(request, self.template_name, {
            'form': form,
            'date_from': date_from,
            'date_to': date_to,
            'queryset': self.queryset, 
            'obj_name': obj_name,
            'app_name': app_name,
            'model': model,
        })

    def post(self, request, *args, **kwargs):

        obj_name = self.model._meta.verbose_name.lower().replace(" ", "")
        app_name = self.model._meta.app_label
        model = self.model

        form = DateRangeForm(request.POST)

        if form.is_valid():

            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            self.queryset = self.queryset.filter(owner=request.user, tr_date__gte=date_from, tr_date__lte=date_to )

            form = DateRangeForm()

            return render(request, self.template_name, {
                'form': form,
                'date_from': date_from,
                'date_to': date_to,
                'queryset': self.queryset,            
                'obj_name': obj_name,
                'app_name': app_name,
                'model': model,
            })

        return render(request, self.template_name, {
            'form': form,
            'obj_name': obj_name,
            'app_name': app_name,
            'model': model,
        })


class ChequingTransactionSearchResults(BaseItemsSearchresults):
    queryset = ChequingTransaction.objects.all().prefetch_related('account', 'tags',)
    table = ChequingTransactionTable
    filter = ChequingTransactionFilter


class ChequingTransactionDetail(DetailView):
    template_name = template_path + "chq_tr_detail.html"
    model = ChequingTransaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expense_records = ExpenseRecord.objects.filter(chq_tr=self.object)
        context['expense_records'] = expense_records

        return context


class ChequingTransactionCreate(BaseItemCreateWithPopup):
    model = ChequingTransaction
    form_class = ChequingTransactionForm
    template_name = template_path + "chq_tr_form.html"
    template_name_popup = template_path + "chq_tr_form_popup.html"
    cancel_button_url = reverse_lazy('bankexp:chequingtransaction_list')


class ChequingTransactionEdit(BaseItemEdit):
    model = ChequingTransaction
    form_class = ChequingTransactionForm
    template_name = template_path + "chq_tr_form.html"


class ChequingTransactionDelete(BaseItemDelete):
    model = ChequingTransaction
    template_name = template_path + "chq_tr_confirm_delete.html"
    success_url = reverse_lazy('bankexp:chequingtransaction_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exp_recs_count = self.object.exp_recs.all().count()
        context['exp_recs_count'] = exp_recs_count
        return context


class ChequingTransactionImport(TransactionImportView):

    model = ChequingTransaction
    resource_class = ChequingTransactionResource
    template_name = template_path + "chq_tr_import.html"
    success_url = reverse_lazy('bankexp:chequingtransaction_list')
    formats = (base_formats.CSV, base_formats.XLS,)

    def create_dataset(self, *args, **kwargs):
        """ 
        Insert owner and account fields into the data.
        """  

        dataset = super().create_dataset(*args, **kwargs)
        length = len(dataset._data)
        dataset.append_col([self.request.user.username] * length,
                           header="owner")
        dataset.append_col([self.account] * length,
                           header="account")    

        return dataset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_accounts = ChequingAccount.objects.filter(owner=self.request.user)
        context['user_accounts'] = user_accounts
        context['model'] = self.model
    
        return context
    

class ChequingTransactionExport(ExportView):

    resource_class = ChequingTransactionResource
    model = ChequingTransaction
    template_name = template_path + "chq_tr_export.html"
    formats = (base_formats.CSV, base_formats.XLS,)

    def get_queryset(self):
        return ChequingTransaction.objects.filter(owner=self.request.user)


# Credit Card Transaction Views #############################################   

class CreditCardTransactionTableView(View):
    """
    A class to display the credit card transactions (using datatables)
    It still uses the url for list even that the template displays 
    the table with transactions.
    """

    template_name = template_path + "cc_tr_table.html"
    model = CreditCardTransaction
    queryset = CreditCardTransaction.objects.all().prefetch_related('account', 'tags',)

    def get(self, request):

        current_date = date.today()
        date_from = current_date + timedelta(-180)
        date_to = current_date
        self.queryset = self.queryset.filter(owner=request.user, tr_date__gte=date_from, tr_date__lte=date_to )

        form = DateRangeForm()
        
        obj_name = self.model._meta.verbose_name.lower().replace(" ", "")
        app_name = self.model._meta.app_label
        model = self.model

        return render(request, self.template_name, {
            'form': form,
            'date_from': date_from,
            'date_to': date_to,
            'queryset': self.queryset, 
            'obj_name': obj_name,
            'app_name': app_name,
            'model': model,
        })

    def post(self, request, *args, **kwargs):

        obj_name = self.model._meta.verbose_name.lower().replace(" ", "")
        app_name = self.model._meta.app_label
        model = self.model

        form = DateRangeForm(request.POST)

        if form.is_valid():

            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            self.queryset = self.queryset.filter(owner=request.user, tr_date__gte=date_from, tr_date__lte=date_to )

            form = DateRangeForm()

            return render(request, self.template_name, {
                'form': form,
                'date_from': date_from,
                'date_to': date_to,
                'queryset': self.queryset,            
                'obj_name': obj_name,
                'app_name': app_name,
                'model': model,
            })

        return render(request, self.template_name, {
            'form': form,
            'obj_name': obj_name,
            'app_name': app_name,
            'model': model,
        })


class CreditCardTransactionSearchResultsList(BaseItemsSearchresults):
    queryset = CreditCardTransaction.objects.all().prefetch_related('account', 'tags',)
    table = CreditCardTransactionTable
    filter = CreditCardTransactionFilter


class CreditCardTransactionDetail(DetailView):
    template_name = template_path + "cc_tr_detail.html"
    model = CreditCardTransaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expense_records = ExpenseRecord.objects.filter(cc_tr=self.object)
        context['expense_records'] = expense_records

        return context


class CreditCardTransactionCreate(BaseItemCreateWithPopup):
    model = CreditCardTransaction
    form_class = CreditCardTransactionForm
    template_name = template_path + "cc_tr_form.html"
    template_name_popup = template_path + "cc_tr_form_popup.html"
    cancel_button_url = reverse_lazy('bankexp:creditcardtransaction_list')


class CreditCardTransactionEdit(BaseItemEdit):
    model = CreditCardTransaction
    form_class = CreditCardTransactionForm
    template_name = template_path + "cc_tr_form.html"


class CreditCardTransactionDelete(BaseItemDelete):
    model = CreditCardTransaction
    template_name = template_path + "cc_tr_confirm_delete.html"
    success_url = reverse_lazy('bankexp:creditcardtransaction_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exp_recs_count = self.object.exp_recs.all().count()
        context['exp_recs_count'] = exp_recs_count
        return context

   
class CreditCardTransactionImport(TransactionImportView):

    model = CreditCardTransaction
    resource_class = CreditCardTransactionResource
    template_name = template_path + "cc_tr_import.html"
    success_url = reverse_lazy('bankexp:creditcardtransaction_list')
    formats = (base_formats.CSV, base_formats.XLS,)

    def create_dataset(self, *args, **kwargs):
        """ 
        Insert owner and account fields into the data.
        """  

        dataset = super().create_dataset(*args, **kwargs)
        length = len(dataset._data)
        dataset.append_col([self.request.user.username] * length,
                           header="owner")
        dataset.append_col([self.account] * length,
                           header="account")    

        return dataset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_accounts = CreditCardAccount.objects.filter(owner=self.request.user)
        context['user_accounts'] = user_accounts
        context['model'] = self.model
    
        return context
    
 
class CreditCardTransactionExport(ExportView):

    resource_class = CreditCardTransactionResource
    model = CreditCardTransaction
    template_name = template_path + "cc_tr_export.html"
    formats = (base_formats.CSV, base_formats.XLS,)

    def get_queryset(self):
        return CreditCardTransaction.objects.filter(owner=self.request.user)


# Expense Type Views ###########################################

class ExpenseTypeList(BaseItemsList):
    model = ExpenseType


class ExpenseTypeSearchResults(BaseItemsSearchresults):
    queryset = ExpenseType.objects.all()
    table = ExpenseTypeTable
    filter = ExpenseTypeFilter


class ExpenseTypeDetail(DetailView):
    template_name = template_path + "expense_type_detail.html"
    model = ExpenseType

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exp_recs = ExpenseRecord.objects.filter(
            owner=self.request.user, 
            exp_type=self.object.id
            ).prefetch_related('exp_type', 'location', 'chq_tr','cc_tr')

        if exp_recs:

            exp_rec_amnt = 0
            exp_recs_years = []

            for item in exp_recs:

                if item.amount != None:
                    exp_rec_amnt += item.amount

                exp_rec_year = item.exp_date.year
                if exp_rec_year not in exp_recs_years:
                    exp_recs_years.append(exp_rec_year)

            exp_recs_years_totals = []
            exp_recs_years_records = []

            for year in exp_recs_years:
                year_amounts = []
                year_dict_total_amounts = {}

                year_records_amounts = []
                year_dict_records_amounts = {}

                for item in exp_recs:
                    exp_rec_year = item.exp_date.year

                    if item.amount != None:
                        if exp_rec_year == year:
                            year_amounts.append(item.amount)
                            year_records_amounts.append(item)

                total_year_amount = sum(year_amounts)
                year_dict_total_amounts[year] = total_year_amount
                exp_recs_years_totals.append(year_dict_total_amounts)

                year_dict_records_amounts[year] = year_records_amounts
                exp_recs_years_records.append(year_dict_records_amounts)

            context['exp_rec_amnt'] = exp_rec_amnt
            context['exp_recs_years_totals'] = exp_recs_years_totals
            context['exp_recs_years_records'] = exp_recs_years_records

        context['exp_recs'] = exp_recs
        
        return context


class ExpenseTypeCreate(BaseItemCreateWithPopup):
    model = ExpenseType
    form_class = ExpenseTypeForm
    template_name = template_path + "expense_type_form.html"
    template_name_popup = template_path + "expense_type_form_popup.html"
    cancel_button_url = reverse_lazy('bankexp:expensetype_list')


class ExpenseTypeEdit(BaseItemEdit):
    model = ExpenseType
    form_class = ExpenseTypeForm
    template_name = template_path + "expense_type_form.html"


class ExpenseTypeDelete(BaseItemDelete):
    model = ExpenseType
    template_name = template_path + "expense_type_confirm_delete.html"
    success_url = reverse_lazy('bankexp:expensetype_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exp_recs_count = self.object.exp_recs.all().count()
        context['exp_recs_count'] = exp_recs_count
        return context


class ExpenseTypeImport(ImportView):

    model = ExpenseType
    resource_class = ExpenseTypeResource
    template_name = template_path + "expense_type_import.html"
    success_url = reverse_lazy('bankexp:expensetype_list')
    formats = (base_formats.CSV, base_formats.XLS,)

    
    def get_queryset(self):
        return ExpenseType.objects.filter(owner=self.request.user)
        

    def create_dataset(self, *args, **kwargs):
        """ 
        Insert owner and account fields into the data.
        """  

        dataset = super().create_dataset(*args, **kwargs)
        length = len(dataset._data)
        dataset.append_col([self.request.user.username] * length,
                           header="owner")   

        return dataset
    

class ExpenseTypeExport(ExportView):

    resource_class = ExpenseTypeResource
    model = ExpenseType
    template_name = template_path + "expense_type_export.html"
    formats = (base_formats.CSV, base_formats.XLS,)

    def get_queryset(self):
        return ExpenseType.objects.filter(owner=self.request.user)



# Location Views ######################################################

class LocationList(BaseItemsList):
    model = Location


class LocationSearchResults(BaseItemsSearchresults):
    queryset = Location.objects.all()
    table = LocationTable
    filter = LocationFilter


class LocationDetail(DetailView):
    template_name = template_path + "location_detail.html"
    model = Location

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exp_recs = ExpenseRecord.objects.filter(
            owner=self.request.user, 
            location=self.object.id
            ).prefetch_related('exp_type', 'location', 'chq_tr', 'cc_tr')

        if exp_recs:

            exp_rec_amnt = 0
            exp_recs_years = []

            for item in exp_recs:

                if item.amount != None:
                    exp_rec_amnt += item.amount

                exp_rec_year = item.exp_date.year
                if exp_rec_year not in exp_recs_years:
                    exp_recs_years.append(exp_rec_year)

            exp_recs_years_totals = []
            exp_recs_years_records = []

            for year in exp_recs_years:
                year_amounts = []
                year_dict_total_amounts = {}

                year_records_amounts = []
                year_dict_records_amounts = {}

                for item in exp_recs:
                    exp_rec_year = item.exp_date.year

                    if item.amount != None:
                        if exp_rec_year == year:
                            year_amounts.append(item.amount)
                            year_records_amounts.append(item)


                total_year_amount = sum(year_amounts)
                year_dict_total_amounts[year] = total_year_amount
                exp_recs_years_totals.append(year_dict_total_amounts)

                year_dict_records_amounts[year] = year_records_amounts
                exp_recs_years_records.append(year_dict_records_amounts)

            context['exp_rec_amnt'] = exp_rec_amnt
            context['exp_recs_years_totals'] = exp_recs_years_totals
            context['exp_recs_years_records'] = exp_recs_years_records

        context['exp_recs'] = exp_recs
        
        return context


class LocationCreate(BaseItemCreateWithPopup):
    model = Location
    form_class = LocationForm
    template_name = template_path + "location_form.html"
    template_name_popup = template_path + "location_form_popup.html"
    cancel_button_url = reverse_lazy('bankexp:location_list')


class LocationEdit(BaseItemEdit):
    model = Location
    form_class = LocationForm
    template_name = template_path + "location_form.html"


class LocationDelete(BaseItemDelete):
    model = Location
    template_name = template_path + "location_confirm_delete.html"
    success_url = reverse_lazy('bankexp:location_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exp_recs_count = self.object.exp_recs.all().count()
        context['exp_recs_count'] = exp_recs_count
        return context


class LocationImport(ImportView):
    model = Location
    resource_class = LocationResource
    template_name = template_path + "location_import.html"
    success_url = reverse_lazy('bankexp:location_list')
    formats = (base_formats.CSV, base_formats.XLS,)

    
    def get_queryset(self):
        return Location.objects.filter(owner=self.request.user)
        

    def create_dataset(self, *args, **kwargs):
        """ 
        Insert owner and account fields into the data.
        """  

        dataset = super().create_dataset(*args, **kwargs)
        length = len(dataset._data)
        dataset.append_col([self.request.user.username] * length,
                           header="owner")   

        return dataset
    

class LocationExport(ExportView):
    resource_class = LocationResource
    model = Location
    template_name = template_path + "location_export.html"
    formats = (base_formats.CSV, base_formats.XLS,)

    def get_queryset(self):
        return Location.objects.filter(owner=self.request.user)


# Expense Record Views ################################################ 

class ExpenseRecordList(ListView):
    template_name = template_path + "expense_record_list.html"
    model = ExpenseRecord

    def get(self, request):
        self.queryset = self.model.objects.filter(owner=request.user).prefetch_related('exp_type', 'location', 'chq_tr','cc_tr')
                
        obj_name = self.model._meta.verbose_name.lower().replace(" ", "")
        app_name = self.model._meta.app_label

        return render(request, self.template_name, {
            'queryset': self.queryset,
            'obj_name': obj_name,
            'app_name': app_name,
            'model': self.model,
        })


class ExpenseRecordSearchResults(BaseItemsSearchresults):
    queryset = ExpenseRecord.objects.all().prefetch_related(
                        'exp_type',
                        'location',
                        'chq_tr',
                        'cc_tr',
                        'location')
    table = ExpenseRecordTable
    filter = ExpenseRecordFilter


class ExpenseRecordDetail(DetailView):
    template_name = template_path + "expense_record_detail.html"
    model = ExpenseRecord


class ExpenseRecordCreate(BaseItemCreateWithPopup):
    model = ExpenseRecord
    form_class = ExpenseRecordForm
    template_name = template_path + "expense_record_form.html"
    cancel_button_url = reverse_lazy('bankexp:expenserecord_list')

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial_data = {k: self.request.GET[k] for k in self.request.GET}
        initial = initial_data
      
        return initial


class ExpenseRecordEdit(BaseItemEdit):
    model = ExpenseRecord
    form_class = ExpenseRecordForm
    template_name = template_path + "expense_record_form.html"


class ExpenseRecordDelete(BaseItemDelete):
    model = ExpenseRecord
    template_name = template_path + "expense_record_confirm_delete.html"
    success_url = reverse_lazy('bankexp:expenserecord_list')


class ExpenseRecordImport(ImportView):

    model = ExpenseRecord
    resource_class = ExpenseRecordResource
    template_name = template_path + "expense_record_import.html"
    success_url = reverse_lazy('bankexp:expenserecord_list')
    formats = (base_formats.CSV, base_formats.XLS,)

    
    def get_queryset(self):
        return ExpenseRecord.objects.filter(owner=self.request.user)
        
    def create_dataset(self, *args, **kwargs):
        """ 
        Insert owner and account fields into the data.
        """  

        dataset = super().create_dataset(*args, **kwargs)
        length = len(dataset._data)
        dataset.append_col([self.request.user.username] * length,
                           header="owner") 

        return dataset
    

class ExpenseRecordExport(ExportView):
    resource_class = ExpenseRecordResource
    model = ExpenseRecord
    template_name = template_path + "expense_record_export.html"
    formats = (base_formats.CSV, base_formats.XLS,)

    def get_queryset(self):
        return ExpenseRecord.objects.filter(owner=self.request.user)


# Tag Views ########################################################

class TagList(BaseItemsList):
    model = Tag
    template_name = template_path + "tag_list.html"

class TagSearchResults(BaseItemsSearchresults):
    queryset = Tag.objects.all()
    table = TagTable
    filter = TagFilter


class TagDetail(DetailView):
    template_name = template_path + "tag_detail.html"
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Processing chequing transactions which have this Tag
        # Getting the transactions and extracting the years in a list
        chq_trs = self.object.chq_trs.all().filter(owner=self.request.user).prefetch_related('account', 'tags',)

        if chq_trs:

            chq_tr_withdrawal = 0   # total withdrawals for all years
            chq_tr_deposits = 0     # total deposits for all years
            chq_tr_years = []       # all the years when transactions occured
            
            for item in chq_trs:

                if item.tr_withdrawal != None:
                    chq_tr_withdrawal += item.tr_withdrawal

                if item.tr_deposits != None:
                    chq_tr_deposits += item.tr_deposits            
                
                chq_tr_year = item.tr_date.year
                if chq_tr_year not in chq_tr_years:
                    chq_tr_years.append(chq_tr_year)

            
            # Getting the totals per year for chequing transactions 
            # and storing the transactions per year for this Tag
            # in a list of dictionaries. The year dictionary has as key the year
            # and as value a list of transactions for that year

            chq_trs_years_totals_withdrawals = []
            chq_trs_years_transactions_withdrawals = []

            chq_trs_years_totals_deposits = []
            chq_trs_years_transactions_deposits = []
                
            for year in chq_tr_years:

                year_withdrawals = []
                year_dict_total_withdrawals = {}            
                
                year_transactions_withdrawals = []
                year_dict_transactions_withdrawals = {}
                
                year_deposits = []
                year_dict_total_deposits = {}            
                            
                year_transactions_deposits = []
                year_dict_transactions_deposits = {}
                

                for item in chq_trs:
                    chq_tr_year = item.tr_date.year
                    
                    if item.tr_withdrawal != None:
                                    
                        if chq_tr_year == year:
                            year_withdrawals.append(item.tr_withdrawal)
                            year_transactions_withdrawals.append(item)

                    if item.tr_deposits != None:
                                    
                        if chq_tr_year == year:
                            year_deposits.append(item.tr_deposits)
                            year_transactions_deposits.append(item)    
                

                total_year_withdrawal = sum(year_withdrawals)           
                year_dict_total_withdrawals[year] = total_year_withdrawal 
                chq_trs_years_totals_withdrawals.append(year_dict_total_withdrawals)

                year_dict_transactions_withdrawals[year] = year_transactions_withdrawals
                chq_trs_years_transactions_withdrawals.append(year_dict_transactions_withdrawals)

                total_year_deposits = sum(year_deposits) 
                year_dict_total_deposits[year] = total_year_deposits
                chq_trs_years_totals_deposits.append(year_dict_total_deposits)
                    
                year_dict_transactions_deposits[year] = year_transactions_deposits
                chq_trs_years_transactions_deposits.append(year_dict_transactions_deposits)

            context['chq_tr_withdrawal'] = chq_tr_withdrawal
            context['chq_tr_deposits'] = chq_tr_deposits
            context['chq_trs_years_totals_withdrawals'] = chq_trs_years_totals_withdrawals
            context['chq_trs_years_transactions_withdrawals'] = chq_trs_years_transactions_withdrawals
            context['chq_trs_years_totals_deposits'] = chq_trs_years_totals_deposits
            context['chq_trs_years_transactions_deposits'] = chq_trs_years_transactions_deposits


        # Processing credit card transactions which have this Transaction Tag
        # Getting the transactions and extracting the years in a list
        cc_trs = self.object.cc_trs.all().filter(owner=self.request.user).prefetch_related('account', 'tags',)

        if cc_trs:
            cc_tr_debit = 0 # total debits for all years
            cc_tr_credit = 0 # total credits for all years
            cc_tr_years = [] # all the years when transactions occured

            for item in cc_trs:

                if item.tr_debit != None:
                    cc_tr_debit += item.tr_debit

                if item.tr_credit != None:
                    cc_tr_credit += item.tr_credit

                cc_tr_year = item.tr_date.year
                if cc_tr_year not in cc_tr_years:
                    cc_tr_years.append(cc_tr_year)

            cc_trs_years_totals_debits = []
            cc_trs_years_transactions_debits = []

            cc_trs_years_totals_credits = []
            cc_trs_years_transactions_credits = []

            for year in cc_tr_years:

                year_debits = []
                year_dict_total_debits = {}            
                
                year_transactions_debits = []
                year_dict_transactions_debits = {}
                
                year_credits = []
                year_dict_total_credits = {}            
                            
                year_transactions_credits = []
                year_dict_transactions_credits = {}

                for item in cc_trs:
                    cc_tr_year = item.tr_date.year

                    if item.tr_debit != None:
                                    
                        if cc_tr_year == year:
                            year_debits.append(item.tr_debit)
                            year_transactions_debits.append(item)

                    if item.tr_credit != None:
                                    
                        if cc_tr_year == year:
                            year_credits.append(item.tr_credit)
                            year_transactions_credits.append(item)

                total_year_debits = sum(year_debits)           
                year_dict_total_debits[year] = total_year_debits 
                cc_trs_years_totals_debits.append(year_dict_total_debits)

                year_dict_transactions_debits[year] = year_transactions_debits
                cc_trs_years_transactions_debits.append(year_dict_transactions_debits)

                total_year_credits = sum(year_credits) 
                year_dict_total_credits[year] = total_year_credits
                cc_trs_years_totals_credits.append(year_dict_total_credits)

                year_dict_transactions_credits[year] = year_transactions_credits
                cc_trs_years_transactions_credits.append(year_dict_transactions_credits)

            context['cc_tr_debit'] = cc_tr_debit
            context['cc_tr_credit'] = cc_tr_credit
            context['cc_trs_years_totals_debits'] = cc_trs_years_totals_debits
            context['cc_trs_years_transactions_debits'] = cc_trs_years_transactions_debits
            context['cc_trs_years_totals_credits'] = cc_trs_years_totals_credits
            context['cc_trs_years_transactions_credits'] = cc_trs_years_transactions_credits 
        
        return context


class TagCreate(BaseItemCreateWithPopup):
    model = Tag
    form_class = TagForm
    template_name = template_path + "tag_form.html"
    template_name_popup = template_path + "tag_form_popup.html"
    cancel_button_url = reverse_lazy('bankexp:tag_list')


class TagEdit(BaseItemEdit):
    model = Tag
    form_class = TagForm
    template_name = template_path + "tag_form.html"


class TagDelete(BaseItemDelete):
    model = Tag
    template_name = template_path + "tag_confirm_delete.html"
    success_url = reverse_lazy('bankexp:tag_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chq_trs_count = self.object.chq_trs.all().count()
        cc_trs_count = self.object.cc_trs.all().count()
        context['chq_trs_count'] = chq_trs_count
        context['cc_trs_count'] = cc_trs_count
        return context


class TagMultipleAssign(FormView):
    template_name = template_path + "tag_multiple_assign.html"
    form_class = TagMultipleAssignForm
    success_url = reverse_lazy('bankexp:tag_multiple_assign')
    extra_context = {}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form, **kwargs):

        string_expr = form.cleaned_data['string_expr']
        tag_choice = form.cleaned_data['tag']

        self.assign_tag(string_expr, tag_choice)

        return super().form_valid(form)


    def assign_tag(self, string_expr, tag_choice):

        owner = self.request.user

        # Assigning the tag_choice to chequing transactions
        # Filtering by string expression (string_expr) in the
        # transaction description (tr_desc)
        chq_trs = ChequingTransaction.objects.filter(
            owner=owner, 
            tr_desc__icontains = string_expr).prefetch_related('account', 'tags',)

        for tr in chq_trs:
            tr_tags = tr.tags.all()
            if tag_choice not in tr_tags:
                tr.tags.add(tag_choice)

        # Assigning the tag_choice to credit card transactions
        # Filtering by string expression (string_expr) in the
        # transaction description (tr_desc)
        cc_trs = CreditCardTransaction.objects.filter(
            owner=owner, 
            tr_desc__icontains = string_expr).prefetch_related('account', 'tags',)

        for tr in cc_trs:
            tr_tags = tr.tags.all()
            if tag_choice not in tr_tags:
                tr.tags.add(tag_choice)      

        self.extra_context['string_expr'] = string_expr
        self.extra_context['tag_choice'] = tag_choice

   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context.update(self.extra_context)      

        if self.extra_context:
           tag_choice = self.extra_context['tag_choice']
           chq_tr_tagged = ChequingTransaction.objects.filter(tags = tag_choice).prefetch_related('account', 'tags',)
           context['chq_tr_tagged'] = chq_tr_tagged
           cc_tr_tagged = CreditCardTransaction.objects.filter(tags = tag_choice).prefetch_related('account', 'tags',)
           context['cc_tr_tagged'] = cc_tr_tagged

        # Clearing the extra_content dictionary 
        # as to not be cached to the next view
        TagMultipleAssign.extra_context=dict()
                   
        return context


class TagMultipleRemove(FormView):
    template_name = template_path + "tag_multiple_remove.html"
    form_class = TagMultipleRemoveForm
    success_url = reverse_lazy('bankexp:tag_multiple_remove')
    extra_context = {}

    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        
        tag_choice = form.cleaned_data['tag']
        self.remove_tag(tag_choice)

        return super().form_valid(form)

    def remove_tag(self, tag_choice, **kwargs):
        # Getting all the chequing transactions which have the tag from tag_choice
        chq_trs = ChequingTransaction.objects.filter(tags = tag_choice).prefetch_related('account', 'tags',)

        chq_trs_tag_removed = []

        for tr in chq_trs:
            tr_tags = tr.tags.all()
            
            if tag_choice in tr_tags:
                tr.tags.remove(tag_choice)
                chq_trs_tag_removed.append(tr)

        # Getting all the credit card transactions which have the tag from tag_choice
        cc_trs = CreditCardTransaction.objects.filter(tags = tag_choice).prefetch_related('account', 'tags',)

        cc_trs_tag_removed = []

        for tr in cc_trs:
            tr_tags = tr.tags.all()
            
            if tag_choice in tr_tags:
                tr.tags.remove(tag_choice)
                cc_trs_tag_removed.append(tr)        

        self.extra_context['tag_choice'] = tag_choice
        self.extra_context['chq_trs_tag_removed'] = chq_trs_tag_removed
        self.extra_context['cc_trs_tag_removed'] = cc_trs_tag_removed
               
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context.update(self.extra_context)  

        # Clearing the extra_content dictionary as to not be cached
        # to the next view
        TagMultipleRemove.extra_context=dict()
                   
        return context


class TagImport(ImportView):
    model = Tag
    resource_class = TagResource
    template_name = template_path + "tag_import.html"
    success_url = reverse_lazy('bankexp:tag_list')
    formats = (base_formats.CSV, base_formats.XLS,)

    
    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)
        
    def create_dataset(self, *args, **kwargs):
        """ 
        Insert owner and account fields into the data.
        """  

        dataset = super().create_dataset(*args, **kwargs)
        length = len(dataset._data)
        dataset.append_col([self.request.user.username] * length,
                           header="owner")   

        return dataset
    

class TagExport(ExportView):
    resource_class = TagResource
    model = Tag
    template_name = template_path + "tag_export.html"
    formats = (base_formats.CSV, base_formats.XLS,)

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)

