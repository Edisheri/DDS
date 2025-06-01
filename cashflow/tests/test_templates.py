from django.test import TestCase
from django.urls import reverse


class TemplateTests(TestCase):
    """Tests for verifying template rendering and content."""

    def test_base_template_extends(self):
        """Verify base template structure and required content."""
        response = self.client.get(reverse('record_list'))
        
        # Check template inheritance
        self.assertTemplateUsed(response, 'base.html')
        
        # Verify essential content exists
        self.assertContains(response, 'Cash Flow Manager')

    def test_add_record_template_fields(self):
        """Verify all required form fields are present in the add record template."""
        response = self.client.get(reverse('add_record'))
        
        # List of expected form field names
        required_fields = [
            'date',
            'amount',
            'status',
            'type',
            'category',
            'subcategory',
            'comment'
        ]
        
        # Check each required field exists in the template
        for field in required_fields:
            self.assertContains(response, f'name="{field}"')