import unittest
from app import app, DATA_DIR
from cms.utils import list_data_files

class AppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)

        expected_files = list_data_files(DATA_DIR)

        for file_name in expected_files:
            with self.subTest(file=file_name):
                self.assertIn(file_name, html)
    
    def test_file_contents(self):

        file_names = list_data_files(DATA_DIR)

        for files in file_names:
            response = self.client.get(f"/files/{files}")
            content = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()