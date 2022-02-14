from django.test import TestCase
from django.test import Client
from common.libraries.tear_down import tear_down

class PageTest(TestCase):
    """Base class for client-access page automated test cases."""
    fixtures = [
        'test/auth__user',
        'test/relationships__email',
        'test/relationships__phone_number_type',
        'test/relationships__phone_number',
        'test/relationships__user',
        'test/common__country'
    ]

    def setUp(
            self,
            url : str,
            method : str
        ):
        """TestCase setUp method with additonal parameters for overriding.

        Parameters
        ----------
        url
            URL to access
        method
            'get' if HTTP GET, 'post' if HTTP POST
        """
        c = Client()
        if method == 'get':
            self.response = c.get(url)
        elif method == 'post':
            self.response = c.post(url)
        super().setUp()

    def tearDown(self):
        tear_down()

    def assert_contains(
            self,
            content : str
        ):
        """Assert content is contained in response.

        content : str
            Content to assert.
        """
        self.assertContains(self.response, content)