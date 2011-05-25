import unittest


class DashboardTests(unittest.TestCase):

    def setUp(self):
        from medleydash.webapp import app
        self.app = app.test_client()

    def test_combined(self):
        rv = self.app.get('/')
        assert 200 == rv.status_code
        assert "<h2>Ave. Cycle Time</h2>" in rv.data
        assert "<title>Medley Development Dashboard</title>" in rv.data
        assert "<th>cycletime</th>" in rv.data

if __name__ == "__main__":
    unittest.main()
