from tests.test_helper import *
from datetime import date
from braintree.dispute import Dispute

class TestDispute(unittest.TestCase):
    legacy_attributes = {
            "transaction": {
                "id": "transaction_id",
                "amount": "100.00",
            },
            "id": "123456",
            "currency_iso_code": "USD",
            "status": "open",
            "amount": "100.00",
            "received_date": date(2013, 4, 10),
            "reply_by_date": date(2013, 4, 10),
            "reason": "fraud",
            "transaction_ids": ["asdf", "qwer"],
            "date_opened": date(2013, 4, 1),
            "date_won": date(2013, 4, 2),
            "kind": "chargeback",
        }

    attributes = {
            "amount": "100.00",
            "amount_disputed": "100.00",
            "amount_won": "0.00",
            "case_number": "CB123456",
            "created_at": datetime(2013, 4, 10, 10, 50, 39),
            "currency_iso_code": "USD",
            "date_opened": date(2013, 4, 1),
            "date_won": date(2013, 4, 2),
            "forwarded_comments": "Forwarded comments",
            "id": "123456",
            "kind": "chargeback",
            "merchant_account_id": "abc123",
            "original_dispute_id": "original_dispute_id",
            "reason": "fraud",
            "reason_code": "83",
            "reason_description": "Reason code 83 description",
            "received_date": date(2013, 4, 10),
            "reference_number": "123456",
            "reply_by_date": date(2013, 4, 17),
            "status": "open",
            "updated_at": datetime(2013, 4, 10, 10, 50, 39),
            "evidence": [
                {
                    "comment": None,
                    "created_at": datetime(2013, 4, 11, 10, 50, 39),
                    "id": "evidence1",
                    "sent_to_processor_at": None,
                    "url": "url_of_file_evidence",
                },
                {
                    "comment": "text evidence",
                    "created_at": datetime(2013, 4, 11, 10, 50, 39),
                    "id": "evidence2",
                    "sent_to_processor_at": "2009-04-11",
                    "url": None,
                },
            ],
            "status_history": [
                {
                    "effective_date": "2013-04-10",
                    "status": "open",
                    "timestamp": datetime(2013, 4, 10, 10, 50, 39),
                },
            ],
            "transaction": {
                "id": "transaction_id",
                "amount": "100.00",
                "created_at": datetime(2013, 3, 19, 10, 50, 39),
                "order_id": None,
                "purchase_order_number": "po",
                "payment_instrument_subtype": "Visa",
            },
        }

    def test_legacy_constructor(self):
        dispute = Dispute(dict(self.legacy_attributes))

        self.assertEqual(dispute.id, "123456")
        self.assertEqual(dispute.amount, Decimal("100.00"))
        self.assertEqual(dispute.currency_iso_code, "USD")
        self.assertEqual(dispute.reason, Dispute.Reason.Fraud)
        self.assertEqual(dispute.status, Dispute.Status.Open)
        self.assertEqual(dispute.transaction_details.id, "transaction_id")
        self.assertEqual(dispute.transaction_details.amount, Decimal("100.00"))
        self.assertEqual(dispute.date_opened, date(2013, 4, 1))
        self.assertEqual(dispute.date_won, date(2013, 4, 2))
        self.assertEqual(dispute.kind, Dispute.Kind.Chargeback)

    def test_legacy_params_with_new_attributes(self):
        dispute = Dispute(dict(self.attributes))

        self.assertEqual(dispute.id, "123456")
        self.assertEqual(dispute.amount, Decimal("100.00"))
        self.assertEqual(dispute.currency_iso_code, "USD")
        self.assertEqual(dispute.reason, Dispute.Reason.Fraud)
        self.assertEqual(dispute.status, Dispute.Status.Open)
        self.assertEqual(dispute.transaction_details.id, "transaction_id")
        self.assertEqual(dispute.transaction_details.amount, Decimal("100.00"))
        self.assertEqual(dispute.date_opened, date(2013, 4, 1))
        self.assertEqual(dispute.date_won, date(2013, 4, 2))
        self.assertEqual(dispute.kind, Dispute.Kind.Chargeback)

    def test_constructor_populates_new_fields(self):
        attributes = dict(self.attributes)
        del attributes["amount"]

        dispute = Dispute(attributes)

        self.assertEqual(dispute.amount_disputed, 100.0)
        self.assertEqual(dispute.amount_won, 0.00)
        self.assertEqual(dispute.case_number, "CB123456")
        self.assertEqual(dispute.created_at, datetime(2013, 4, 10, 10, 50, 39))
        self.assertEqual(dispute.forwarded_comments, "Forwarded comments")
        self.assertEqual(dispute.merchant_account_id, "abc123")
        self.assertEqual(dispute.original_dispute_id, "original_dispute_id")
        self.assertEqual(dispute.reason_code, "83")
        self.assertEqual(dispute.reason_description, "Reason code 83 description")
        self.assertEqual(dispute.reference_number, "123456")
        self.assertEqual(dispute.updated_at, datetime(2013, 4, 10, 10, 50, 39))
        self.assertIsNone(dispute.evidence[0].comment)
        self.assertEqual(dispute.evidence[0].created_at, datetime(2013, 4, 11, 10, 50, 39))
        self.assertEqual(dispute.evidence[0].id, "evidence1")
        self.assertIsNone(dispute.evidence[0].sent_to_processor_at)
        self.assertEqual(dispute.evidence[0].url, "url_of_file_evidence")
        self.assertEqual(dispute.evidence[1].comment, "text evidence")
        self.assertEqual(dispute.evidence[1].created_at, datetime(2013, 4, 11, 10, 50, 39))
        self.assertEqual(dispute.evidence[1].id, "evidence2")
        self.assertEqual(dispute.evidence[1].sent_to_processor_at, "2009-04-11")
        self.assertIsNone(dispute.evidence[1].url)
        self.assertEqual(dispute.status_history[0].effective_date, "2013-04-10")
        self.assertEqual(dispute.status_history[0].status, "open")
        self.assertEqual(dispute.status_history[0].timestamp, datetime(2013, 4, 10, 10, 50, 39))

    def test_constructor_handles_none_fields(self):
        attributes = dict(self.attributes)
        attributes.update({
            "amount": None,
            "date_opened": None,
            "date_won": None,
            "evidence": None,
            "reply_by_date": None,
            "status_history": None
        })

        dispute = Dispute(attributes)

        self.assertIsNone(dispute.reply_by_date)
        self.assertIsNone(dispute.amount)
        self.assertIsNone(dispute.date_opened)
        self.assertIsNone(dispute.date_won)
        self.assertIsNone(dispute.status_history)

    def test_constructor_populates_transaction(self):
        dispute = Dispute(dict(self.attributes))

        self.assertEqual(dispute.transaction.id, "transaction_id")
        self.assertEqual(dispute.transaction.amount, Decimal("100.00"))
        self.assertEqual(dispute.transaction.created_at, datetime(2013, 3, 19, 10, 50, 39))
        self.assertIsNone(dispute.transaction.order_id)
        self.assertEqual(dispute.transaction.purchase_order_number, "po")
        self.assertEqual(dispute.transaction.payment_instrument_subtype, "Visa")

    @raises_with_regexp(NotFoundError, "dispute with id None not found")
    def test_finding_none_raises_not_found_exception(self):
        Dispute.find(None)

    @raises_with_regexp(NotFoundError, "dispute with id ' ' not found")
    def test_finding_empty_id_raises_not_found_exception(self):
        Dispute.find(" ")
