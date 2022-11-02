from django.shortcuts import render

from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import escape, escapejs
from django.urls import reverse
from django.db.models.deletion import ProtectedError

from django_tables2 import RequestConfig

from collections import OrderedDict

from .forms import SearchForm

from bankexp.models import (
    ChequingAccount, CreditCardAccount, ChequingTransaction, CreditCardTransaction,
    ExpenseType, Location, ExpenseRecord, Tag)
from bankexp.filters import (ChequingAccountFilter, CreditCardAccountFilter, ChequingTransactionFilter, CreditCardTransactionFilter, 
    ExpenseTypeFilter, ExpenseRecordFilter, TagFilter, LocationFilter)
from bankexp.tables import (ChequingAccountTable, CreditCardAccountTable, ChequingTransactionTable, CreditCardTransactionTable, 
    ExpenseTypeTable, ExpenseRecordTable, TagTable, LocationTable)

template_path = 'base/'




# Base Views ########################################################

class BaseItemsList(ListView):
    """
    Base class view used to display the items as list or as boxes
    Subclassing ListView to make use of pagination.
    As template, it can use the template which displya the items as boxes
    or a template which displays the items as a list of links.
    """
    model = None
    template_name = template_path + 'base_items_list_boxes.html'
    paginate_by = 18

    
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Getting the object name, lower, and with spaces between words
        # removed so it can be used with add button templatetag
        # Also getting the app name to use in the add button templatetag
        context['obj_name'] = self.model._meta.verbose_name.lower().replace(" ", "")
        context['app_name'] = self.model._meta.app_label
        context['model'] = self.model

        return context


class BaseItemsSearchresults(View):
    """
    Base class view used to display the search as table using django-tables2
    The queyset is filtered by the user
    """
    queryset = None
    table = None
    filter = None
    template_name = template_path + "base_search_results.html"


    def get(self, request):
        
        queryset = self.queryset.filter(owner=request.user)   

        if self.filter:
            queryset = self.filter(request.GET, queryset).qs

        table = self.table(queryset, orderable=False)
        
        paginate = {'paginator_class': Paginator, 'per_page': 15}
        RequestConfig(request, paginate).configure(table)
                
        return render(request, self.template_name, {
            'table': table,
            'model': self.queryset.model,
        }) 


class BaseItemCreate(CreateView):
    """
    Base class view used for item creation when popup is not needed
    """
    model = None
    form_class = None
    template_name = None
    cancel_button_url = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        kwargs['instance'] = self.model(owner=self.request.user)

        return kwargs
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user   
        self.object.save()

        return super().form_valid(form) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name
        context['cancel_button_url'] = self.cancel_button_url
        return context


class BaseItemCreateWithPopup(CreateView):
    """
    Base class view used for item creation with popup window.
    This is for those items that are ForeigKey for a model and can be created from 
    a popup window in the specific model
    """
    model = None
    form_class = None
    template_name = None
    template_name_popup = None
    cancel_button_url = None


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        kwargs['instance'] = self.model(owner=self.request.user)

        return kwargs
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user   
        self.object.save()

        return super().form_valid(form)  
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name
        context['cancel_button_url'] = self.cancel_button_url

        if ('_popup' in self.request.GET):
            self.template_name = self.template_name_popup
            context['popup'] = self.request.GET['_popup'] 
        return context

      
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if "_popup" in request.POST:
            if self.object: 
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                    (escape(self.object.pk), escapejs(self.object)))

        return response


class BaseItemEdit(UpdateView):
    """
    Base class view used for item editiong
    """
    model = None
    form_class = None
    template_name = None


    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name
        return context


class BaseItemDelete(DeleteView):
    """
    Base class view for item deletion. The get_context_data method will 
    add new context items depending on dependencies of each model instance
    """
    model = None
    template_name = None
    success_url = None

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['obj_type'] = self.model._meta.verbose_name
        
        return context

    def form_valid(self, form):
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            context = self.get_context_data(
                object=self.object,
                error="<strong> {0} </strong> cannot be deleted!".format(self.object)
            )
            return self.render_to_response(context) 
        return HttpResponseRedirect(success_url)


# ##########################################################################

class HomePageView(View):
    template_name = template_path + "home.html"

    def get(self, request):
        user_chq_acc_count = ChequingAccount.objects.filter(owner=self.request.user).count()
        user_cc_acc_count = CreditCardAccount.objects.filter(owner=self.request.user).count()
        user_chq_trs_count = ChequingTransaction.objects.filter(owner=self.request.user).count()
        user_cc_trs_count = CreditCardTransaction.objects.filter(owner=self.request.user).count()
        user_exp_types_count = ExpenseType.objects.filter(owner=self.request.user).count()
        user_exp_recs_count = ExpenseRecord.objects.filter(owner=self.request.user).count()
        user_locs_count = Location.objects.filter(owner=self.request.user).count()
        user_tags_count = Tag.objects.filter(owner=self.request.user).count()
        
        user_chq_accs_dict = {}
        user_chq_accs = ChequingAccount.objects.filter(owner=self.request.user)
        
        for item in user_chq_accs:
            item_chq_trs = ChequingTransaction.objects.filter(owner=self.request.user, account=item)
            item_chq_trs_count = item_chq_trs.count()
            user_chq_accs_dict[item] = item_chq_trs_count

        user_cc_accs_dict = {}
        user_cc_accs = CreditCardAccount.objects.filter(owner=self.request.user)
        
        for item in user_cc_accs:
            item_cc_trs = CreditCardTransaction.objects.filter(owner=self.request.user, account=item)
            item_cc_trs_count = item_cc_trs.count()
            
            user_cc_accs_dict[item] = item_cc_trs_count            

        return render(request, self.template_name, {
            'user_chq_acc_count': user_chq_acc_count,
            'user_cc_acc_count': user_cc_acc_count,
            'user_chq_trs_count': user_chq_trs_count,
            'user_cc_trs_count': user_cc_trs_count,
            'user_exp_types_count': user_exp_types_count,
            'user_exp_recs_count': user_exp_recs_count,
            'user_locs_count': user_locs_count,
            'user_tags_count': user_tags_count,
            'user_chq_accs_dict': user_chq_accs_dict,
            'user_cc_accs_dict': user_cc_accs_dict,
        })


# Errors Views ################################################################################

def custom_page_not_found_view(request, exception):
    return render(request, "base/errors/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "base/errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "base/errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "base/errors/400.html", {})


# SearchView #############################################################

SEARCH_MAX_RESULTS = 10

class SearchView(View):
    template_name = template_path + "search/search.html"


    def get(self, request):

        SEARCH_TYPES = OrderedDict((
            ('chequingaccount', {
                    'queryset': ChequingAccount.objects.filter(owner=self.request.user),
                    'filter': ChequingAccountFilter,
                    'table': ChequingAccountTable,
                    'url': 'bankexp:chequingaccount_search'
            }),
            ('creditcardaccount', {
                    'queryset': CreditCardAccount.objects.filter(owner=self.request.user),
                    'filter': CreditCardAccountFilter,
                    'table': CreditCardAccountTable,
                    'url': 'bankexp:creditcardaccount_search'
            }),
            ('chequingtransaction', {
                    'queryset': ChequingTransaction.objects.filter(owner=self.request.user).prefetch_related('account', 'tags',),
                    'filter': ChequingTransactionFilter,
                    'table': ChequingTransactionTable,
                    'url': 'bankexp:chequingtransaction_search'
            }),
            ('creditcardtransaction', {
                    'queryset': CreditCardTransaction.objects.filter(owner=self.request.user).prefetch_related('account', 'tags',),
                    'filter': CreditCardTransactionFilter,
                    'table': CreditCardTransactionTable,
                    'url': 'bankexp:creditcardtransaction_search'
            }),
            ('expensetype', {
                    'queryset': ExpenseType.objects.filter(owner=self.request.user),
                    'filter': ExpenseTypeFilter,
                    'table': ExpenseTypeTable,
                    'url': 'bankexp:expensetype_search'
            }),
            ('expenserecord', {
                    'queryset': ExpenseRecord.objects.filter(owner=self.request.user).prefetch_related(
                        'exp_type',
                        'location',
                        'chq_tr',
                        'cc_tr',
                        'location'),
                    'filter': ExpenseRecordFilter,
                    'table': ExpenseRecordTable,
                    'url': 'bankexp:expenserecord_search'
            }),
            ('tag', {
                    'queryset': Tag.objects.filter(owner=self.request.user),
                    'filter': TagFilter,
                    'table': TagTable,
                    'url': 'bankexp:tag_search'
            }),
            ('location', {
                    'queryset': Location.objects.filter(owner=self.request.user),
                    'filter': LocationFilter,
                    'table': LocationTable,
                    'url': 'bankexp:location_search'
            }),
        ))

        if 'q' not in request.GET:
            return render(request, self.template_name, { 'form': SearchForm(), })

        form = SearchForm(request.GET)
        results = []

        if form.is_valid():

            if form.cleaned_data['obj_type']:
                obj_types = [form.cleaned_data['obj_type']]

            else:
                obj_types = SEARCH_TYPES.keys()

            for obj_type in obj_types:
                
                queryset = SEARCH_TYPES[obj_type]['queryset']
                filter_cls = SEARCH_TYPES[obj_type]['filter']
                table = SEARCH_TYPES[obj_type]['table']
                url = SEARCH_TYPES[obj_type]['url']

                filtered_queryset = filter_cls({'q': form.cleaned_data['q']}, queryset=queryset).qs
                table = table(filtered_queryset, orderable=False)
                table.paginate(per_page=SEARCH_MAX_RESULTS)

                if table.page:
                    results.append({
                        'name': queryset.model._meta.verbose_name_plural,
                        'table': table,
                        'url': '{}?q={}'.format(reverse(url), form.cleaned_data['q']),
                    })

        return render(request, self.template_name, {
            'form': form,
            'results': results,
        })



