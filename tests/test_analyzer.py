import unittest
from core.analyzer import analyze_records


class AnalyzerTests(unittest.TestCase):
    def test_aggregates(self):
        result = analyze_records([
            {"ip": "1.1.1.1", "url": "/", "method": "GET", "status": 200, "size": 100},
            {"ip": "1.1.1.1", "url": "/x", "method": "POST", "status": 500, "size": 50},
        ])
        self.assertEqual(result["total_requests"], 2)
        self.assertEqual(result["error_requests"], 1)
        self.assertEqual(result["total_bytes"], 150)


if __name__ == "__main__":
    unittest.main()
