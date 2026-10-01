from unittest.mock import patch

from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase


CONTACT_URL = "/api/contact/send/"


@override_settings(
    RESEND_API_KEY="test-resend-key",
    DEFAULT_FROM_EMAIL="Byteprowler <hello@example.com>",
    CONTACT_RECEIVER_EMAIL="owner@example.com",
)
class ContactEmailViewTests(APITestCase):
    def test_contact_submission_sends_notification_and_acknowledgement(self):
        payload = {
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "subject": "Project inquiry",
            "message": "Can we work together?",
        }

        with patch("contact.views.resend.Emails.send") as send_email:
            response = self.client.post(CONTACT_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {"success": True, "message": "Transmission secure. Message received."},
        )
        self.assertEqual(send_email.call_count, 2)

        notification_payload = send_email.call_args_list[0].args[0]
        acknowledgement_payload = send_email.call_args_list[1].args[0]

        self.assertEqual(notification_payload["to"], ["owner@example.com"])
        self.assertEqual(notification_payload["reply_to"], "ada@example.com")
        self.assertEqual(acknowledgement_payload["to"], ["ada@example.com"])
        self.assertEqual(acknowledgement_payload["reply_to"], "owner@example.com")
        self.assertIn("Thanks for reaching out to Byteprowler", acknowledgement_payload["html"])

    def test_missing_required_fields_returns_clean_validation_error(self):
        response = self.client.post(
            CONTACT_URL,
            {"name": "Ada Lovelace", "email": "ada@example.com", "subject": ""},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"success": False, "message": "Please provide all required fields."},
        )

    def test_acknowledgement_failure_does_not_fail_submission(self):
        payload = {
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "subject": "Project inquiry",
            "message": "Can we work together?",
        }

        with (
            patch(
                "contact.views.resend.Emails.send",
                side_effect=[{"id": "notification-email"}, Exception("ack failed")],
            ) as send_email,
            patch("contact.views.logger.exception") as log_exception,
        ):
            response = self.client.post(CONTACT_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {"success": True, "message": "Transmission secure. Message received."},
        )
        self.assertEqual(send_email.call_count, 2)
        log_exception.assert_called_once_with("Failed to send contact acknowledgement email.")

    def test_notification_failure_returns_clean_server_error(self):
        payload = {
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "subject": "Project inquiry",
            "message": "Can we work together?",
        }

        with (
            patch("contact.views.resend.Emails.send", side_effect=Exception("provider failed")),
            patch("contact.views.logger.exception") as log_exception,
        ):
            response = self.client.post(CONTACT_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(
            response.json(),
            {
                "success": False,
                "message": "Message could not be sent. Please try again later.",
            },
        )
        log_exception.assert_called_once_with("Failed to send contact email.")
