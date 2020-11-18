from django.test import TestCase

class UnitTestCase(TestCase):
    def test_home_page_loaded(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")