from app import app

import unittest

class FlaskTestCase(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/',content_type='html/text')
        self.assertEqual(response.status_code,200)
    def test_404(self):
        tester = app.test_client(self)
        response = tester.get('/doesnotexist',content_type='html/text')
        self.assertEqual(response.status_code,404)
    def test_index_form(self):
        tester = app.test_client(self)
        response = tester.post('/start',data=dict(scope='https://google.com'),follow_redirects = True)
        self.assertEqual(response.status_code,200)
    def test_vuln_no_exists(self):
        tester = app.test_client(self)
        response = tester.get('/vulnerability/100000',content_type='html/text')
        self.assertEqual(response.status_code,500)


if __name__ == "__main__":
    unittest.main()