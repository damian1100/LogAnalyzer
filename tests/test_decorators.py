import unittest
from core.config import LogConfig
from core.parser import LogParser
from utils.decorators import retry


class DecoratorTests(unittest.TestCase):
    def test_retry_rejects_invalid_arguments(self):
        with self.assertRaises(ValueError):
            retry(attempts=0)

    def test_method_requires_config(self):
        parser = LogParser.__new__(LogParser)
        parser.config = None
        with self.assertRaises(RuntimeError):
            parser.parse_line("anything")

    def test_config_property(self):
        config = LogConfig()
        with self.assertRaises(ValueError):
            config.max_file_size_mb = -1


if __name__ == "__main__":
    unittest.main()
