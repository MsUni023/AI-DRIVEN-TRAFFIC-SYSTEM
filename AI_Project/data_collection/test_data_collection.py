import unittest
from data_collection import fetch_real_time_data

class TestDataCollection(unittest.TestCase):
    def test_fetch_real_time_data(self):
        # Mock API key, origin, and destination for testing
        api_key = 'AIzaSyBQYjXlvE8dfD4RXEXAzXeJwRIFIEHDTlY'
        origin = 'Maseno'
        destination = 'Nairobi'
        data = fetch_real_time_data(api_key, origin, destination)
        self.assertIn('routes', data)

if __name__ == '__main__':
    unittest.main()
