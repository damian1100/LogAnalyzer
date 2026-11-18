import tempfile
import unittest
from pathlib import Path

from core.config import LogConfig
from core.parser import parse_file, parse_lines
from utils.patterns import is_valid_ipv4

SAMPLE = '127.0.0.1 - - [10/Oct/2025:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 1024'


class ParserTests(unittest.TestCase):
    def test_parse_line_generator(self):
        records = list(parse_lines(iter([SAMPLE, "not a log line"])))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["status"], 200)
        self.assertEqual(records[0]["url"], "/index.html")

    def test_parse_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "access.log"
            path.write_text(SAMPLE + "\n", encoding="utf-8")
            self.assertEqual(len(list(parse_file(path))), 1)

    def test_strict_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.log"
            path.write_text("bad\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                list(parse_file(path, LogConfig(strict=True)))

    def test_ipv4(self):
        self.assertTrue(is_valid_ipv4("192.168.1.1"))
        self.assertFalse(is_valid_ipv4("999.1.1.1"))


if __name__ == "__main__":
    unittest.main()
