from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CashFlowRecord


class CashFlowForm(forms.ModelForm):
    """
    Comprehensive form for creating and updating CashFlowRecord entries.
    
    Features:
    - Custom widget configurations with Bootstrap styling
    - Dynamic field validation for financial data
    - Support for required relationship fields
    - Localized placeholder text
    - Client-side date picker integration
    """

    class Meta:
        model = CashFlowRecord
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'id': 'date-select'
                }
            ),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'amount-select',
                'placeholder': _('Enter amount...'),
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'comment-select',
                'rows': '4',
                'placeholder': _('Write something...'),
            }),
        }

    def __init__(self, *args, **kwargs):
        """Initialize form with consistent styling for all fields."""
        super().__init__(*args, **kwargs)
        
        # Apply consistent select field styling
        select_fields = {
            'status': 'status-select',
            'type': 'type-select',
            'category': 'category-select',
            'subcategory': 'subcategory-select'
        }
        
        for field_name, field_id in select_fields.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-select form-select-sm',
                    'id': field_id
                })

    def clean_amount(self):
        """Validate that transaction amount is positive.
        
        Returns:
            Decimal: Validated amount value
            
        Raises:
            ValidationError: If amount is zero or negative
        """
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise forms.ValidationError(
                _("Amount must be greater than zero")
            )
        return amount

    def clean(self):
        """Validate required relationship fields.
        
        Returns:
            dict: Cleaned form data
            
        Raises:
            ValidationError: If any required field is missing
        """
        cleaned_data = super().clean()
        
        required_relations = [
            'status',
            'type',
            'category',
            'subcategory'
        ]
        
        for field in required_relations:
            if not cleaned_data.get(field):
                self.add_error(
                    field,
                    _("This selection is required")
                )
                
        return cleaned_data