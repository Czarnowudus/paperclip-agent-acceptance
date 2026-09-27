import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "sum-cli"


def run(args=None):
    return subprocess.run(
        [sys.executable, str(CLI)] + (args or []),
        capture_output=True,
        text=True,
    )


class SumCliTest(unittest.TestCase):
    def test_valid_two_integers(self):
        self.assertEqual(run(["2", "3"]).stdout, "5\n")
        self.assertEqual(run(["-7", "10"]).stdout, "3\n")

    def test_large_integers(self):
        self.assertEqual(
            run(["100000000000000000000", "1"]).stdout,
            "100000000000000000001\n",
        )

    def test_no_arguments(self):
        self.assertNotEqual(run([]).returncode, 0)

    def test_one_argument(self):
        self.assertNotEqual(run(["1"]).returncode, 0)

    def test_three_arguments(self):
        self.assertNotEqual(run(["1", "2", "3"]).returncode, 0)

    def test_non_integer_alpha(self):
        p = run(["abc", "1"])
        self.assertNotEqual(p.returncode, 0)

    def test_non_integer_float(self):
        p = run(["1.5", "2"])
        self.assertNotEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main()
