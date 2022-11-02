import django_filters
from django.db.models import Q

from .models import (
    ChequingAccount, CreditCardAccount, ChequingTransaction, CreditCardTransaction,
    ExpenseType, Location, ExpenseRecord, Tag)




class ChequingAccountFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = ChequingAccount
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) )


class CreditCardAccountFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = CreditCardAccount
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) )


class ChequingTransactionFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = ChequingTransaction
        fields = ['account', 'tr_desc', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(  Q(tr_desc__icontains=value) | Q(account__name__icontains=value) )


class CreditCardTransactionFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = CreditCardTransaction
        fields = ['account', 'tr_desc', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(  Q(tr_desc__icontains=value) | Q(account__name__icontains=value) )


class ExpenseTypeFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = ExpenseType
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) )


class LocationFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Location
        fields = ['name', 'address']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) |
                               Q(address__icontains=value))

class ExpenseRecordFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = ExpenseRecord
        fields = ['exp_type',  ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(exp_type__name__icontains=value) |
                               Q(location__name__icontains=value) |
                               Q(details__icontains=value) |
                               Q(chq_tr__tr_desc__icontains=value) |
                               Q(cc_tr__tr_desc__icontains=value) 
                               )


class TagFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', lookup_expr='in')

    class Meta:
        model = Tag
        fields = ['name', ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) )