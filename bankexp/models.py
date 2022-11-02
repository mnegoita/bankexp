from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from ckeditor_uploader.fields import RichTextUploadingField




class ChequingAccount(models.Model):
    """ A class representing a Chequing Account """

    name = models.CharField(max_length=200, verbose_name = "Account Name")  
    notes = RichTextUploadingField(blank=True, default = '')
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Chequing Account"
        verbose_name_plural = 'Chequing Accounts'
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields = ['owner', 'name', ],
                name = 'unique_owner_name_chequingaccount'
            )
        ]

    def get_absolute_url(self):
        return "/chequingaccounts/{0}/".format(self.id)

    
class CreditCardAccount(models.Model):
    """ A class representing a Credit Card Account """

    name = models.CharField(max_length=200, verbose_name = "Account Name")  
    notes = RichTextUploadingField(blank=True, default = '')
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Credit Card Account"
        verbose_name_plural = 'Credit Card Accounts'
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields = ['owner', 'name', ],
                name = 'unique_owner_name_creditcardaccount'
            )
        ]

    def get_absolute_url(self):
        return "/creditcardaccounts/{0}/".format(self.id)


class Tag(models.Model):
    """ 
    A class representing a Tag.
    The idea for this model would be to mark a transaction 
    (chequing or credit card) so these 
    can be displayed together in the tag detail.
    """

    name = models.CharField(max_length=200)
    notes = RichTextUploadingField(blank=True, default = '')
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = 'Tags'
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields = ['owner', 'name', ],
                name = 'unique_owner_name_tag'
            )
        ]

    def get_absolute_url(self):
        return "/tags/{0}/".format(self.id)


class ChequingTransaction(models.Model):
    """ A class representing a Chequing Transaction """
    
    account = models.ForeignKey(
        ChequingAccount, 
        related_name = 'transactions', 
        related_query_name = 'transaction',
        verbose_name = "Account",
        on_delete=models.PROTECT)
    tr_date = models.DateField(verbose_name = "Date", help_text = "Transaction Date")
    tr_desc = models.CharField(max_length=200, verbose_name = "Description")
    tr_withdrawal = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        validators=[MinValueValidator(0.001)],
        blank = True, null = True,
        verbose_name = "Withdrawal")
    tr_deposits = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        validators=[MinValueValidator(0.001)],
        blank = True, null = True,
        verbose_name = "Deposits")
    tr_balance = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        verbose_name = "Balance",
        help_text = "Transaction Balance")
    tags = models.ManyToManyField(
        Tag,
        related_name = "chq_trs",
        related_query_name = "chq_tr",
        verbose_name = "Tags",
        blank=True)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Chequing Transaction"
        verbose_name_plural = 'Chequing Transactions'
        ordering = ["-tr_date"]
        constraints = [
            models.UniqueConstraint(
                fields = [
                    'owner',
                    'account', 
                    'tr_date',
                    'tr_desc',
                    'tr_withdrawal',
                    'tr_deposits',
                    'tr_balance',
                    ],
                name = 'unique_fields_chequingtransaction'
            )
        ]

    def get_absolute_url(self):
        return "/chequingtransactions/{0}/".format(self.id)

    def __str__(self):
        string_name = f" {self.tr_desc} "
        return string_name


class CreditCardTransaction(models.Model):
    """ A class representing a Credit Card Transaction """
    
    account = models.ForeignKey(
        CreditCardAccount, 
        related_name = 'transactions', 
        related_query_name = 'transaction',
        verbose_name = "Account",
        on_delete=models.PROTECT)
    tr_date = models.DateField(verbose_name = "Date", help_text = "Transaction Date")
    tr_desc = models.CharField(max_length=200, verbose_name = "Description")
    tr_debit = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        validators=[MinValueValidator(0.001)],
        blank = True, null = True,
        verbose_name = "Debit")
    tr_credit = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        validators=[MinValueValidator(0.001)],
        blank = True, null = True,
        verbose_name = "Credit")
    tr_balance = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        verbose_name = "Balance",
        help_text = "Transaction Balance")
    tags = models.ManyToManyField(
        Tag,
        related_name = "cc_trs",
        related_query_name = "cc_tr",
        verbose_name = "Tags",
        blank=True)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Credit Card Transaction"
        verbose_name_plural = 'Credit Card Transactions'
        ordering = ["-tr_date"]
        constraints = [
            models.UniqueConstraint(
                fields = [
                    'owner',
                    'account', 
                    'tr_date',
                    'tr_desc',
                    'tr_debit',
                    'tr_credit',
                    'tr_balance',
                    ],
                name = 'unique_fields_creditcardtransaction'
            )
        ]

    def get_absolute_url(self):
        return "/creditcardtransactions/{0}/".format(self.id)

    def __str__(self):
        string_name = f" {self.tr_desc} "
        return string_name


class ExpenseType(models.Model):
    """ A class representing a type of expense like Gas, Paint.
    The Expense Type is tied to an expense record. 
    """
    
    name = models.CharField(max_length=200, verbose_name = "Expense")
    notes = RichTextUploadingField(blank=True, default = '')
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Expense Type"
        verbose_name_plural = 'Expense Types'
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields = ['owner', 'name',],
                name = 'unique_owner_name_expensetype'
            )
        ]

    def get_absolute_url(self):
        return "/expensetypes/{0}/".format(self.id)


class Location(models.Model):
    """Class representing a location for an expense record"""
    name = models.CharField(max_length=200, help_text = "Like Walmart, Costco")
    address = models.CharField(max_length=200, blank=True)
    prov_st = models.CharField(max_length=20, blank=True, verbose_name = "Province/State")
    country = models.CharField(max_length=20, blank=True)
    notes = RichTextUploadingField(blank=True, default = '')
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = 'Locations'
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields = [ 'owner', 'name', 'address',],
                name = 'unique_owner_name_address_location'
            )
        ]
        
    def get_absolute_url(self):
        return "/locations/{0}/".format(self.id)


class ExpenseRecord(models.Model):
    """A class reprenting an expense record tied to an expense type.
    There can be several expense reconrds on one transaction.
    """
    exp_type = models.ForeignKey(
        ExpenseType, 
        related_name = 'exp_recs', 
        related_query_name = 'exp_rec',
        verbose_name = "Expense Type",
        on_delete=models.PROTECT)
    exp_date = models.DateField(verbose_name = "Expense Date",) 
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        validators=[MinValueValidator(0.01)])
    tax = models.DecimalField(
        max_digits=7, 
        decimal_places=3, 
        validators=[MinValueValidator(0.01)], 
        blank=True, 
        null=True) 
    location = models.ForeignKey(
        Location, 
        related_name = 'exp_recs', 
        related_query_name = 'exp_rec',
        on_delete=models.SET_NULL,
        default = '',
        blank = True,
        null = True,)
    chq_tr = models.ForeignKey(
        ChequingTransaction, 
        related_name = 'exp_recs', 
        related_query_name = 'exp_rec',
        verbose_name = "Chequing Transaction",
        blank = True,
        null = True,
        on_delete=models.PROTECT)
    cc_tr = models.ForeignKey(
        CreditCardTransaction, 
        related_name = 'exp_recs', 
        related_query_name = 'exp_rec',
        verbose_name = "Credit Card Transaction",
        blank = True,
        null = True,
        on_delete=models.PROTECT)
    quantity = models.CharField(max_length=20, blank=True, default = '')
    details = RichTextUploadingField(blank=True, default = '', verbose_name = "Record Details")
    files = models.FileField(upload_to='media/expenses/', blank=True, null=True) # expenses directory in media directory
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    clone_fields = [
                    'exp_type',
                    'exp_date',
                    'amount',
                    'tax',
                    'location',
                    'chq_tr',
                    'cc_tr',
                    ]

    def get_absolute_url(self):
        return "/expenserecords/{0}/".format(self.id)

    def __str__(self):
        return "{0}: {1} (${2})".format(self.exp_type, self.exp_date, self.amount)

    class Meta:
        verbose_name = "Expense Record"
        verbose_name_plural = 'Expense Records'
        ordering = ["-exp_date"]
        constraints = [
            models.UniqueConstraint(
                fields = [
                    'owner', 
                    'exp_type',
                    'exp_date',
                    'amount',
                    'location',
                    'chq_tr',
                    'cc_tr',
                    'quantity',
                    ],
                name = 'unique_fields_expenserecord'
            )
        ]

    def clean(self):

        # There can be only a chequing transaction or a credit card transaction but not both
        if self.chq_tr and self.cc_tr:
            raise ValidationError(mark_safe( f"There can be only a chequing transaction or a credit card transaction but not both" )) 
        if self.cc_tr and self.chq_tr:
            raise ValidationError(mark_safe( f"There can be only a chequing transaction or a credit card transaction but not both" )) 

        if self.chq_tr:
            if self.exp_date != self.chq_tr.tr_date:
                raise ValidationError(mark_safe( f"Expense date {self.exp_date} cannot be different \
                    than transaction date {self.chq_tr.tr_date}" )) 

        if self.cc_tr:
            if self.exp_date != self.cc_tr.tr_date:
                raise ValidationError(mark_safe( f"Expense date {self.exp_date} cannot be different \
                    than transaction date {self.cc_tr.tr_date}" )) 

