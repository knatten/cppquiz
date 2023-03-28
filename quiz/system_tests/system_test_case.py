from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from splinter.browser import Browser


class SystemTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = Browser('django')

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def visit(self, path):
        self.browser.visit(f'{self.live_server_url}{path}')

    def there_is_an_error(self, error_msg, error_id):
        errors = self.browser.find_by_id(error_id + '_errors')[0]
        assert error_msg in errors.text
