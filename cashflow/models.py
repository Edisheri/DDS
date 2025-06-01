from django.db import models
from django.utils import timezone


class Status(models.Model):
    """
    Represents the status/context of a cash flow record (e.g., Business, Personal).
    Used to categorize records by their business relevance.
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    """
    Fundamental classification of cash flow direction.
    Distinguishes between incoming and outgoing funds (Income/Expense).
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Primary classification level for cash flow records.
    Represents broad financial categories (e.g., 'Food', 'Transportation').
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """
    Secondary classification that belongs to a Category.
    Provides more granular tracking (e.g., 'Restaurants' under 'Food').
    """
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CashFlowRecord(models.Model):
    """
    Core financial transaction record tracking all monetary movements.
    Contains complete details including date, classification, and amount.
    """
    date = models.DateField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.amount}"