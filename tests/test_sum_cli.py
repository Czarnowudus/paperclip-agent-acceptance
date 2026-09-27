import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "sum-cli"


def run(args=None, stdin=None):
    return subprocess.run(
        [sys.executable, str(CLI)] + (args or []),
        input=stdin,
        capture_output=True,
        text=True,
    )


class SumCliTest(unittest.TestCase):
    def test_sum_integers(self):
        self.assertEqual(run(["1", "2", "3"]).stdout, "6\n")

    def test_sum_floats(self):
        self.assertEqual(run(["1.5", "2.5"]).stdout, "4.0\n")

    def test_empty_returns_zero(self):
        self.assertEqual(run([]).stdout, "0\n")

    def test_stdin(self):
        self.assertEqual(run(stdin="1\n2\n3\n").stdout, "6\n")

    def test_invalid_number_errors(self):
        p = run(["abc"])
        self.assertEqual(p.returncode, 1)
        self.assertIn("invalid number", p.stderr)

    def test_help(self):
        p = run(["--help"])
        self.assertEqual(p.returncode, 0)
        self.assertIn("Usage", p.stdout)


if __name__ == "__main__":
    unittest.main()