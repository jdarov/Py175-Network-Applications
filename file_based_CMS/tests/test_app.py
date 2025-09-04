import unittest
import shutil
import os
from app import app

class CMSTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.data_path = os.path.join(os.path.dirname(__file__), 'data')
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cms', 'data')
        os.makedirs(self.data_path, exist_ok=True)
    
    def test_index(self):
        self.create_document("about.md")
        self.create_document("changes.txt")

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
        self.assertIn("about.md", response.get_data(as_text=True))
        self.assertIn("changes.txt", response.get_data(as_text=True))
    
    def test_file_contents(self):
        filename = "changes.txt"
        self.create_document(filename)

        with open(f'{self.file_path}/{filename}', 'r') as file:
            contents = file.read()

        response = self.client.get(f"/{filename}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
        self.assertIn(contents, response.get_data(as_text=True))
    
    def tearDown(self):
        return shutil.rmtree(self.data_path, ignore_errors=True)
    def create_document(self, name, content=""):
        with open(os.path.join(self.data_path, name), 'w') as file:
            file.write(content)

if __name__ == "__main__":
    unittest.main()