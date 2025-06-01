from django.test import TestCase, Client
from django.urls import reverse
from cashflow.models import Status, Type, Category, Subcategory, CashFlowRecord


class ViewTests(TestCase):
    """Comprehensive tests for all cashflow views functionality."""

    @classmethod
    def setUpTestData(cls):
        """Create shared test data for all test methods."""
        cls.client = Client()
        cls.status = Status.objects.create(name="TestStatus")
        cls.type = Type.objects.create(name="TestType")
        cls.category = Category.objects.create(name="TestCategory")
        cls.subcategory = Subcategory.objects.create(
            name="TestSubcategory",
            category=cls.category
        )
        
    def setUp(self):
        """Create a test record before each test."""
        self.record = CashFlowRecord.objects.create(
            status=self.status,
            type=self.type,
            category=self.category,
            subcategory=self.subcategory,
            amount=100.00,
            date="2023-01-01"
        )

    def test_record_list_view(self):
        """Verify the record list view displays correct data."""
        response = self.client.get(reverse('record_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cashflow/record_list.html')
        self.assertContains(response, "Cash Flow Records")
        self.assertContains(response, "100.00")

    def test_add_record_view_get(self):
        """Verify the add record form renders correctly."""
        response = self.client.get(reverse('add_record'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cashflow/add_record.html')
        self.assertContains(response, "Add Cash Flow Record")

    def test_edit_record_view_post(self):
        """Verify record editing functionality works correctly."""
        # Create test record
        record = CashFlowRecord.objects.create(
            date='2025-05-10',
            amount=100.00,
            status=self.status,
            type=self.type,
            category=self.category,
            subcategory=self.subcategory,
            comment='Initial comment',
        )
        
        # Prepare updated data
        updated_data = {
            'date': '2025-05-11',
            'amount': 150.00,
            'status': self.status.id,
            'type': self.type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'comment': 'Updated comment',
        }
        
        # Submit update
        response = self.client.post(
            reverse('edit_record', args=[record.id]),
            data=updated_data,
            follow=True
        )
        
        # Verify results
        self.assertEqual(response.status_code, 200)
        record.refresh_from_db()
        self.assertEqual(record.amount, 150.00)
        self.assertEqual(record.comment, 'Updated comment')
        self.assertEqual(record.date.strftime('%Y-%m-%d'), '2025-05-11')

    def test_delete_record_view(self):
        """Verify record deletion functionality works correctly."""
        # Create test record
        record = CashFlowRecord.objects.create(
            date='2025-05-10',
            amount=100.00,
            status=self.status,
            type=self.type,
            category=self.category,
            subcategory=self.subcategory,
            comment='To be deleted',
        )
        
        # Delete record
        response = self.client.post(reverse('delete_record', args=[record.id]))
        
        # Verify deletion
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CashFlowRecord.objects.filter(id=record.id).exists())