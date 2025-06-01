from django.contrib import admin
from .models import Status, Type, Category, Subcategory, CashFlowRecord


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Admin interface configuration for the Status model."""
    
    list_display = ('name',)  # Fields to display in list view
    search_fields = ('name',)  # Fields to enable search functionality


# Standard registration for other models
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(CashFlowRecord)