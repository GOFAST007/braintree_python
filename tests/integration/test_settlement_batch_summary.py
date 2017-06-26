from tests.test_helper import *

class TestSettlementBatchSummary(unittest.TestCase):
    possible_gateway_time_zone_offsets = (5, 4)

    def test_generate_returns_empty_collection_if_there_is_no_data(self):
        result = SettlementBatchSummary.generate('2011-01-01')

        self.assertTrue(result.is_success)
        self.assertEqual([], result.settlement_batch_summary.records)

    def test_generate_returns_error_if_date_can_not_be_parsed(self):
        result = SettlementBatchSummary.generate('THIS AINT NO DATE')
        self.assertFalse(result.is_success)

        settlement_date_errors = result.errors.for_object('settlement_batch_summary').on('settlement_date')
        self.assertEqual(1, len(settlement_date_errors))
        self.assertEqual(ErrorCodes.SettlementBatchSummary.SettlementDateIsInvalid, settlement_date_errors[0].code)

    def test_generate_returns_transactions_settled_on_a_given_day(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": "Sergio Ramos"
            },
            "merchant_account_id": "sandbox_credit_card",
            "options": {"submit_for_settlement": True}
        })

        result = TestHelper.settle_transaction(result.transaction.id)
        settlement_date = result.transaction.settlement_batch_id.split('_')[0]

        result = SettlementBatchSummary.generate(settlement_date)
        self.assertTrue(result.is_success)
        visa_records = [row for row in result.settlement_batch_summary.records
                if row['card_type'] == 'Visa'
                and row['merchant_account_id'] == 'sandbox_credit_card'][0]
        count = int(visa_records['count'])
        self.assertGreaterEqual(count, 1)

    def test_generate_can_be_grouped_by_a_custom_field(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": "Sergio Ramos"
            },
            "options": {"submit_for_settlement": True},
            "custom_fields": {
                "store_me": 1
            }
        })

        result = TestHelper.settle_transaction(result.transaction.id)
        settlement_date = result.transaction.settlement_batch_id.split('_')[0]

        result = SettlementBatchSummary.generate(settlement_date, 'store_me')
        self.assertTrue(result.is_success)
        self.assertTrue('store_me' in result.settlement_batch_summary.records[0])
