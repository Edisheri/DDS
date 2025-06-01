from django.test import TestCase
from cashflow.forms import CashFlowForm
from cashflow.models import Category, Status, Subcategory, Type


class FormTests(TestCase):
    """Test cases for the CashFlowForm validation logic."""
    
    def test_valid_form(self):
        """Test that the form validates with correct input data."""
        # Create required test objects
        status = Status.objects.create(name="Test")
        type = Type.objects.create(name="Test")
        category = Category.objects.create(name="Test")
        subcategory = Subcategory.objects.create(name="Test", category=category)
        
        # Valid form data
        form_data = {
            'status': status.id,
            'type': type.id,
            'category': category.id,
            'subcategory': subcategory.id,
            'amount': '100.00',
            'date': '2023-01-01'
        }
        
        form = CashFlowForm(data=form_data)
        self.assertTrue(form.is_valid(), 
                       f"Form should be valid but has errors: {form.errors}")

    def test_invalid_amount(self):
        """Test that the form rejects non-numeric amount values."""
        form_data = {'amount': 'not_a_number'}
        form = CashFlowForm(data=form_data)
        self.assertFalse(form.is_valid(), 
                         "Form should be invalid with non-numeric amount")