from django.test import TestCase
from django.urls import reverse
from django.utils.translation import activate
from django.conf import settings


class LanguageSwitchTests(TestCase):
    """Tests for language switching functionality."""

    def test_language_switch_to_russian(self):
        """Verify successful switch to Russian language."""
        response = self.client.post(
            reverse('set_language'),
            data={'language': 'ru', 'next': '/'}
        )
        self.assertEqual(response.status_code, 302)
        
        # Verify the page content after language change
        response = self.client.get('/', follow=True)
        self.assertContains(response, 'Денежный поток')

    def test_language_switch_to_english(self):
        """Verify successful switch to English language."""
        response = self.client.post(
            reverse('set_language'),
            data={'language': 'en', 'next': '/'}
        )
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get('/', follow=True)
        self.assertContains(response, 'Cash Flow')


class ViewLanguageTests(TestCase):
    """Tests for view rendering in different languages."""

    def test_view_in_russian(self):
        """Verify view renders correctly in Russian."""
        response = self.client.post(
            '/i18n/setlang/',
            {'language': 'ru', 'next': '/'},
            follow=True
        )
        response = self.client.get('/')
        self.assertContains(response, 'Денежный поток')
        response = self.client.post(
            '/i18n/setlang/',
            {'language': 'en', 'next': '/'},
            follow=True
        )

    def test_view_in_english(self):
        """Verify view renders correctly in English."""
        activate('en')
        response = self.client.get('/')
        self.assertContains(response, 'Cash Flow')


class AcceptLanguageHeaderTests(TestCase):
    """Tests for language detection via Accept-Language header."""

    def test_accept_language_russian(self):
        """Verify Russian language is detected from header."""
        response = self.client.get('/', HTTP_ACCEPT_LANGUAGE='ru')
        self.assertContains(response, 'Денежный поток')

    def test_accept_language_english(self):
        """Verify English language is detected from header."""
        response = self.client.get('/', HTTP_ACCEPT_LANGUAGE='en')
        self.assertContains(response, 'Cash Flow')


class DefaultLanguageTests(TestCase):
    """Tests for default language fallback behavior."""

    def test_default_language(self):
        """Verify correct content is shown for default language."""
        response = self.client.get('/')
        default_language = settings.LANGUAGE_CODE
        
        if default_language.startswith('ru'):
            self.assertContains(response, 'Денежный поток')
        else:
            self.assertContains(response, 'Cash Flow')


class LanguagePersistenceTests(TestCase):
    """Tests for language preference persistence across requests."""

    def test_language_persistence(self):
        """Verify language selection persists between requests."""
        # Set initial language preference
        self.client.post(
            reverse('set_language'),
            data={'language': 'ru', 'next': '/'}
        )
        
        # Verify subsequent request maintains language preference
        response = self.client.get('/')
        self.assertContains(response, 'Денежный поток')