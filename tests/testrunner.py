# per https://stackoverflow.com/questions/28229864/django-manage-py-is-it-possible-to-pass-command-line-argument-for-unit-testin

from django.conf import settings

from django.test.runner import DiscoverRunner

class TestRunner(DiscoverRunner):
    def __init__(self, apikey=None, email=None, templateId=None, **kwargs):
        super().__init__(**kwargs)

        # Message displayed only if one or more tests fail

        print("Email for tests: {}".format(email))
        print("API key for tests: {}".format(apikey))
        print ("template id for tests: {}".format(templateId))

        self.APIKey = apikey
        self.myEmail = email
        self.templateId = templateId

    @classmethod
    def add_arguments(cls, parser):
        DiscoverRunner.add_arguments(parser)

        parser.add_argument('--email', help='Email to send to')
        parser.add_argument('--api-key', dest="apikey", help='API key')
        parser.add_argument('--template-id', dest="templateId", help='GOV notify template id')

    def setup_test_environment(self, **kwargs):
        super(TestRunner, self).setup_test_environment(**kwargs)
        settings.TEST_SETTINGS = {
            'myEmail': self.myEmail,
            'APIKey': self.APIKey,
            'templateId': self.templateId
        }