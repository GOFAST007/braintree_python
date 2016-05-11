from tests.test_helper import *
from braintree.sub_merchant_account.director_details import DirectorDetails

class TestDirectorDetails(unittest.TestCase):
    def test_repr_has_all_fields(self):
        details = DirectorDetails({
            "address": {
                "country": "GBR",
                "locality": "Liverpool",
                "postal_code": "GB 123 456",
                "region": "London",
                "street_address": "123 Main Street",
            },
            "date_of_birth": "1970-01-01",
            "email": "sue@hotmail.com",
            "first_name": "Sue",
            "last_name": "Smith",
            "phone": "555-123-1234",
        })

        regex = "<DirectorDetails {address_details: <AddressDetails {country: 'GBR', locality: 'Liverpool', postal_code: 'GB 123 456', region: 'London', street_address: '123 Main Street'} at \w+>, date_of_birth: '1970-01-01', email: 'sue@hotmail.com', first_name: 'Sue', last_name: 'Smith', phone: '555-123-1234'} at \w+"

        matches = re.match(regex, repr(details))
        self.assertTrue(matches)
