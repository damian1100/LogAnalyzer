import tempfile
import unittest
from pathlib import Path
from core.reader import LogIterator


class ReaderTests(unittest.TestCase):
    def test_iterator_reads_all_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "x.log"
            path.write_text("a\nb\nc\n", encoding="utf-8")
            with LogIterator(path, chunk_size=2) as iterator:
                self.assertEqual(list(iterator), ["a", "b", "c"])

    def test_invalid_chunk_size(self):
        with self.assertRaises(ValueError):
            LogIterator(Path("unused"), 0)


if __name__ == "__main__":
    unittest.main()
