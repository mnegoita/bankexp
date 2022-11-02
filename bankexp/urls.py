from django.urls import path 
from django.contrib.auth.decorators import login_required
from . import views



app_name = 'bankexp'

urlpatterns = [

    # Chequing Accounts Views
    path('chequingaccounts/', login_required(views.ChequingAccountList.as_view()), name='chequingaccount_list'),
    path('chequingaccounts/add/', login_required(views.ChequingAccountCreate.as_view()), name='chequingaccount_add'),
    path('chequingaccounts/export/', login_required(views.ChequingAccountExport.as_view()), name="chequingaccount_export"),
    path('chequingaccounts/import/', login_required(views.ChequingAccountImport.as_view()), name="chequingaccount_import"),
    path('chequingaccounts/import/confirm/', login_required(views.ChequingAccountImport.as_view(confirm=True)), name="chequingaccount_import_confirm"),
    path('chequingaccounts/search-results/', login_required(views.ChequingAccountSearchResults.as_view()), name="chequingaccount_search"),
    path('chequingaccounts/<int:pk>/', login_required(views.ChequingAccountDetail.as_view()), name='chequingaccount'),
    path('chequingaccounts/<int:pk>/edit/', login_required(views.ChequingAccountEdit.as_view()), name='chequingaccount_edit'),
    path('chequingaccounts/<int:pk>/delete/', login_required(views.ChequingAccountDelete.as_view()), name='chequingaccount_delete'),

    # Credit Card Accounts Views
    path('creditcardaccounts/', login_required(views.CreditCardAccountList.as_view()), name='creditcardaccount_list'),
    path('creditcardaccounts/add/', login_required(views.CreditCardAccountCreate.as_view()), name='creditcardaccount_add'),
    path('creditcardaccounts/export/', login_required(views.CreditCardAccountExport.as_view()), name="creditcardaccount_export"),
    path('creditcardaccounts/import/', login_required(views.CreditCardAccountImport.as_view()), name="creditcardaccount_import"),
    path('creditcardaccounts/import/confirm/', login_required(views.CreditCardAccountImport.as_view(confirm=True)), name="creditcardaccount_import_confirm"),
    path('creditcardaccounts/search-results/', login_required(views.CreditCardAccountSearchResults.as_view()), name="creditcardaccount_search"),
    path('creditcardaccounts/<int:pk>/', login_required(views.CreditCardAccountDetail.as_view()), name='creditcardaccount'), 
    path('creditcardaccounts/<int:pk>/edit/', login_required(views.CreditCardAccountEdit.as_view()), name='creditcardaccount_edit'),
    path('creditcardaccounts/<int:pk>/delete/', login_required(views.CreditCardAccountDelete.as_view()), name='creditcardaccount_delete'),

    # Chequing Transactions Views
    path('chequingtransactions/', login_required(views.ChequingTransactionTableView.as_view()), name='chequingtransaction_list'),
    path('chequingtransactions/add/', login_required(views.ChequingTransactionCreate.as_view()), name='chequingtransaction_add'),
    path('chequingtransactions/export/', login_required(views.ChequingTransactionExport.as_view()), name="chequingtransaction_export"),
    path('chequingtransactions/import/', login_required(views.ChequingTransactionImport.as_view()), name="chequingtransaction_import"),
    path('chequingtransactions/import/confirm/', login_required(views.ChequingTransactionImport.as_view(confirm=True)), name="chequingtransaction_import_confirm"),
    path('chequingtransactions/search-results/', login_required(views.ChequingTransactionSearchResults.as_view()), name="chequingtransaction_search"),
    path('chequingtransactions/<int:pk>/', login_required(views.ChequingTransactionDetail.as_view()), name='chequingtransaction'), 
    path('chequingtransactions/<int:pk>/edit/', login_required(views.ChequingTransactionEdit.as_view()), name='chequingtransaction_edit'),
    path('chequingtransactions/<int:pk>/delete/', login_required(views.ChequingTransactionDelete.as_view()), name='chequingtransaction_delete'),

    # Credit Card Transactions Views
    path('creditcardtransactions/', login_required(views.CreditCardTransactionTableView.as_view()), name='creditcardtransaction_list'),
    path('creditcardtransactions/add/', login_required(views.CreditCardTransactionCreate.as_view()), name='creditcardtransaction_add'),
    path('creditcardtransactions/export/', login_required(views.CreditCardTransactionExport.as_view()), name="creditcardtransaction_export"),
    path('creditcardtransactions/import/', login_required(views.CreditCardTransactionImport.as_view()), name="creditcardtransaction_import"),
    path('creditcardtransactions/import/confirm/', login_required(views.CreditCardTransactionImport.as_view(confirm=True)), name="creditcardtransaction_import_confirm"),
    path('creditcardtransactions/search-results/', login_required(views.CreditCardTransactionSearchResultsList.as_view()), name="creditcardtransaction_search"),
    path('creditcardtransactions/<int:pk>/', login_required(views.CreditCardTransactionDetail.as_view()), name='creditcardtransaction'), 
    path('creditcardtransactions/<int:pk>/edit/', login_required(views.CreditCardTransactionEdit.as_view()), name='creditcardtransaction_edit'),
    path('creditcardtransactions/<int:pk>/delete/', login_required(views.CreditCardTransactionDelete.as_view()), name='creditcardtransaction_delete'),

    # Expense Type Views
    path('expensetypes/', login_required(views.ExpenseTypeList.as_view()), name='expensetype_list'),
    path('expensetypes/add/', login_required(views.ExpenseTypeCreate.as_view()), name='expensetype_add'),
    path('expensetypes/export/', login_required(views.ExpenseTypeExport.as_view()), name="expensetype_export"),
    path('expensetypes/import/', login_required(views.ExpenseTypeImport.as_view()), name="expensetype_import"),
    path('expensetypes/import/confirm/', login_required(views.ExpenseTypeImport.as_view(confirm=True)), name="expensetype_import_confirm"),
    path('expensetypes/search-results/', login_required(views.ExpenseTypeSearchResults.as_view()), name="expensetype_search"),
    path('expensetypes/<int:pk>/', login_required(views.ExpenseTypeDetail.as_view()), name='expensetype'),
    path('expensetypes/<int:pk>/edit/', login_required(views.ExpenseTypeEdit.as_view()), name='expensetype_edit'),
    path('expensetypes/<int:pk>/delete/', login_required(views.ExpenseTypeDelete.as_view()), name='expensetype_delete'),

    # Location Views
    path('locations/', login_required(views.LocationList.as_view()), name='location_list'),
    path('locations/add/', login_required(views.LocationCreate.as_view()), name='location_add'),
    path('locations/export/', login_required(views.LocationExport.as_view()), name="location_export"),
    path('locations/import/', login_required(views.LocationImport.as_view()), name="location_import"),
    path('locations/import/confirm/', login_required(views.LocationImport.as_view(confirm=True)), name="location_import_confirm"),
    path('locations/search-results/', login_required(views.LocationSearchResults.as_view()), name="location_search"),
    path('locations/<int:pk>/', login_required(views.LocationDetail.as_view()), name='location'),
    path('locations/<int:pk>/edit/', login_required(views.LocationEdit.as_view()), name='location_edit'),
    path('locations/<int:pk>/delete/', login_required(views.LocationDelete.as_view()), name='location_delete'),

    # Expense Record Views
    path('expenserecords/', login_required(views.ExpenseRecordList.as_view()), name='expenserecord_list'),
    path('expenserecords/add/', login_required(views.ExpenseRecordCreate.as_view()), name='expenserecord_add'),
    path('expenserecords/export/', login_required(views.ExpenseRecordExport.as_view()), name="expenserecord_export"),
    path('expenserecords/import/', login_required(views.ExpenseRecordImport.as_view()), name="expenserecord_import"),
    path('expenserecords/import/confirm/', login_required(views.ExpenseRecordImport.as_view(confirm=True)), name="expenserecord_import_confirm"),
    path('expenserecords/search-results/', login_required(views.ExpenseRecordSearchResults.as_view()), name="expenserecord_search"),
    path('expenserecords/<int:pk>/', login_required(views.ExpenseRecordDetail.as_view()), name='expenserecord'), 
    path('expenserecords/<int:pk>/edit/', login_required(views.ExpenseRecordEdit.as_view()), name='expenserecord_edit'),
    path('expenserecords/<int:pk>/delete/', login_required(views.ExpenseRecordDelete.as_view()), name='expenserecord_delete'),

    # Tag Views
    path('tags/', login_required(views.TagList.as_view()), name='tag_list'),
    path('tags/add/', login_required(views.TagCreate.as_view()), name='tag_add'),
    path('tags/export/', login_required(views.TagExport.as_view()), name="tag_export"),
    path('tags/import/', login_required(views.TagImport.as_view()), name="tag_import"),
    path('tags/import/confirm/', login_required(views.TagImport.as_view(confirm=True)), name="tag_import_confirm"),
    path('tags/search-results/', login_required(views.TagSearchResults.as_view()), name="tag_search"),
    path('tags/tag-multiple-assign/', login_required(views.TagMultipleAssign.as_view()), name='tag_multiple_assign'),
    path('tags/tag-multiple-remove/', login_required(views.TagMultipleRemove.as_view()), name='tag_multiple_remove'),
    path('tags/<int:pk>/', login_required(views.TagDetail.as_view()), name='tag'),
    path('tags/<int:pk>/edit/', login_required(views.TagEdit.as_view()), name='tag_edit'),
    path('tags/<int:pk>/delete/', login_required(views.TagDelete.as_view()), name='tag_delete'),
]


