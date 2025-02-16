import unittest
from data_collection import fetch_real_time_data
from data_preprocessing import preprocess
from routing import calculate_routes
from prediction import predict_traffic

class TestIntegration(unittest.TestCase):
    def test_integration(self):
        api_key = 'AIzaSyBQYjXlvE8dfD4RXEXAzXeJwRIFIEHDTlY'
        origin = 'Maseno'
        destination = 'Nairobi'
        
        # Fetch and process data
        raw_data = fetch_real_time_data(api_key, origin, destination)
        processed_data = preprocess(raw_data)
        
        # Calculate routes and predict traffic
        routes = calculate_routes(origin, destination, processed_data)
        prediction = predict_traffic(processed_data)
        
        # Check results
        self.assertIsNotNone(routes)
        self.assertIn('predicted_duration', prediction)

if __name__ == '__main__':
    unittest.main()
