import unittest


class DashboardTests(unittest.TestCase):

    def setUp(self):
        from medleydash.webapp import app
        self.app = app.test_client()

    def test_combined(self):
        rv = self.app.get('/')
        assert 200 == rv.status_code
        assert "Ave. Cycle Time</h2>" in rv.data
        assert "Medley Development Dashboard</title>" in rv.data
        assert "cycletime</th>" in rv.data

    def test_done(self):
        rv = self.app.get('/done')
        assert 200 == rv.status_code
        assert "cycletime</th>" in rv.data
        assert "doneon</th>" in rv.data

if __name__ == "__main__":
    unittest.main()
