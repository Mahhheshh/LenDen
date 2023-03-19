import django_filters
from django.db.models import Q
from django import forms
from .models import Transactions, PayRequest

class TransactionFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(
        method='filter_search', 
        label="User Email", 
        widget=forms.TextInput(
            attrs={"class": "form-control", 'list': 'user_list'}
            )
        )
    
    is_paid = django_filters.BooleanFilter(
        field_name="is_paid", 
        widget=forms.Select(
            choices=[('', '---'), (True, 'Paid'), (False, 'Not Paid')], 
            attrs={'class': 'form-select'}
            ), 
            label="Status"
        )
    
    type = django_filters.BooleanFilter(
        method="type_filter", 
        widget=forms.Select(
            choices=[('', '---'), (True, 'Loan'), (False, 'Borrow')], 
            attrs={'class': 'form-select'}), 
            label="Type"
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('current_user', None)
        super(TransactionFilter, self).__init__(*args, **kwargs)
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(lender__email__icontains=value) |
            Q(borrower__email__icontains=value)
        )
    
    def type_filter(self, queryset, name, value):
        if value:
            return queryset.filter(lender=self.user)
        return queryset.filter(borrower=self.user)

    class Meta:
        model = Transactions
        fields = ["is_paid"]

class RequestFilter(django_filters.FilterSet):
    request_type = django_filters.BooleanFilter(
        method="type_filter",
        widget=forms.Select(choices=(
            ('', '----'),
            (True, "Sent"),
            (False, "Received")
            ), 
            attrs={"class":"form-select col-md-3"}
        ),
        label="Select Type"
    )
    
    status = django_filters.BooleanFilter(
        field_name="status",
        widget=forms.Select(
            attrs={"class":"form-control"},
            choices=(
                ("", "-----"),
                ('Approved', 'Approved'), 
                ('Pending', 'Pending'), 
                ('Rejected', 'Rejected'),
            ),
        ),
        label="Status",
    )

    amount = django_filters.NumberFilter(
        field_name="amount",
        widget=forms.NumberInput(
            attrs={"class":"form-control"},
        ),
        label="Amount"
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('current_user', None)
        super(RequestFilter, self).__init__(*args, **kwargs)

    def type_filter(self, queryset, name, value):
        if value:
            return queryset.filter(transaction__borrower=self.user)
        return queryset.filter(transaction__lender=self.user)

    class Meta:
        model = PayRequest
        fields = ("status", "amount")