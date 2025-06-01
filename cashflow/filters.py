import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CashFlowRecord


class CashFlowFilter(django_filters.FilterSet):
    """
    Advanced filtering system for CashFlowRecord queries.
    
    Provides comprehensive filtering capabilities including:
    - Date range filtering with custom date picker widgets
    - Exact match filtering for related models (status, type, etc.)
    - Consistent Bootstrap form styling across all filters
    - Localized field labels
    """

    date = django_filters.DateFromToRangeFilter(
        field_name='date',
        label=_('Date Range'),
        widget=django_filters.widgets.RangeWidget(attrs={
            'type': 'date',
            'class': 'form-control form-control-sm'
        })
    )

    class Meta:
        model = CashFlowRecord
        fields = {
            'status': ['exact'],
            'type': ['exact'],
            'category': ['exact'],
            'subcategory': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        """Initialize filters with consistent styling and localized labels."""
        super().__init__(*args, **kwargs)
        
        # Set localized labels for filter fields
        self._set_filter_labels()
        
        # Apply consistent Bootstrap styling to all select inputs
        self._apply_bootstrap_styling()

    def _set_filter_labels(self):
        """Apply translated labels to filter fields."""
        label_mapping = {
            'status': _('Status'),
            'type': _('Type'),
            'category': _('Category'),
            'subcategory': _('Subcategory')
        }
        
        for field_name, label in label_mapping.items():
            if field_name in self.filters:
                self.filters[field_name].label = label

    def _apply_bootstrap_styling(self):
        """Add Bootstrap classes to all filter widgets."""
        for field in self.filters.values():
            if hasattr(field, 'field'):
                widget = field.field.widget
                
                if isinstance(widget, forms.Select):
                    widget.attrs.update({
                        'class': 'form-select form-select-sm'
                    })
                elif isinstance(widget, forms.DateInput):
                    widget.attrs.update({
                        'class': 'form-control form-control-sm'
                    })