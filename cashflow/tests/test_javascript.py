from django.test import LiveServerTestCase
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from cashflow.models import Category, Subcategory


class JSTests(LiveServerTestCase):
    """End-to-end tests for JavaScript functionality using Selenium."""

    @classmethod
    def setUpClass(cls):
        """Initialize the Chrome browser before all tests."""
        super().setUpClass()
        cls.browser = Chrome()
        
    def test_dynamic_subcategory_load(self):
        """Test that subcategories load dynamically based on category selection."""
        # Setup test data
        category = Category.objects.create(name="Test Category")
        Subcategory.objects.create(name="Test Sub", category=category)
        
        # Navigate to the form page
        self.browser.get(f"{self.live_server_url}/add/")
        
        # Select the test category and verify subcategory loading
        category_select = Select(self.browser.find_element(By.ID, 'id_category'))
        category_select.select_by_visible_text("Test Category")
        
        subcategory_select = Select(self.browser.find_element(By.ID, 'id_subcategory'))
        self.assertTrue(subcategory_select.options[1].text, "Test Sub")

    @classmethod
    def tearDownClass(cls):
        """Clean up browser instance after all tests complete."""
        cls.browser.quit()
        super().tearDownClass()