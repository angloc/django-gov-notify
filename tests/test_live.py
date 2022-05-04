from django.conf import settings
from django.core.mail import send_mail, get_connection, EmailMessage
from django.utils.module_loading import import_string
from django.test import TestCase, override_settings

from django_gov_notify.backends import NotifyEmailBackend
from django_gov_notify.message import NotifyEmailMessage

class LiveEmailMessageTest(TestCase):

    def test_live_setup (self):
        assert hasattr (settings, "TEST_SETTINGS"), "TEST_SETTINGS not in Django settings"
        assert "myEmail" in settings.TEST_SETTINGS, "No target email in settings"
        assert "APIKey" in settings.TEST_SETTINGS, "No API key in settings"
        assert "templateId" in settings.TEST_SETTINGS, "No template id in settings"

    def test_live_email_optional (self):
        email = settings.TEST_SETTINGS.get ("myEmail")
        if email is not None:
            APIKey = settings.TEST_SETTINGS.get ("APIKey")
            assert APIKey is not None, "Null API Key"
            templateId = settings.TEST_SETTINGS.get ("templateId")
            assert templateId is not None, "Null template id"
            # See if we can at least go through the motions of sending a live mail.
            # Whether it was received or not is unknown to the test
            with NotifyEmailBackend (
                govuk_notify_api_key=APIKey, 
                fail_silently=False
            ) as connection:
                NotifyEmailMessage (
                    to=[email],
                    connection=connection,
                    template_id=templateId
                ).send ()
