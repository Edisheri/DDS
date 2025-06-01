from django.test import TestCase
from django.urls import reverse


class PerformanceTests(TestCase):
    """Tests for verifying system performance characteristics."""

    def test_record_list_performance(self):
        """Verify the record list view executes within expected query limits."""
        expected_query_count = 5 
        
        with self.assertNumQueries(expected_query_count):
            response = self.client.get(reverse('record_list'))
        self.assertEqual(response.status_code, 200)