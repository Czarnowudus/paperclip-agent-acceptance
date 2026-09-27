import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "sum-cli"
EXAMPLES = ROOT / "examples"


def run(args=None, cwd=None):
    return subprocess.run(
        [sys.executable, str(CLI)] + (args or []),
        capture_output=True,
        text=True,
        cwd=cwd,
    )


class ReadExampleTest(unittest.TestCase):
    def test_hello_txt_success(self):
        p = run(["--read-example", "hello.txt"])
        self.assertEqual(p.returncode, 0)
        self.assertEqual(p.stdout, "hello\n")
        self.assertEqual(p.stderr, "")

    def test_reads_correct_file_from_other_cwd(self):
        # The examples/ root is anchored at the repo directory, not the CWD.
        p = run(["--read-example", "hello.txt"], cwd=tempfile.gettempdir())
        self.assertEqual(p.returncode, 0)
        self.assertEqual(p.stdout, "hello\n")

    def test_missing_file(self):
        p = run(["--read-example", "does_not_exist.txt"])
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, "")

    def test_missing_nested_file(self):
        p = run(["--read-example", "no/such/file.txt"])
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, "")

    def test_directory_rejected(self):
        p = run(["--read-example", "."])
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, "")

    def test_empty_path_rejected(self):
        p = run(["--read-example", ""])
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, "")

    def test_absolute_path_rejected(self):
        p = run(["--read-example", "/etc/passwd"])
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, "")

    def test_parent_traversal_rejected(self):
        p = run(["--read-example", "../README.md"])
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, "")

    def test_deeper_traversal_rejected(self):
        p = run(["--read-example", "subdir/../../README.md"])
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, "")

    def test_traversal_to_missing_file_rejected(self):
        p = run(["--read-example", "../../nonexistent.txt"])
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, "")

    def test_symlink_escape_rejected(self):
        # A symlink inside examples/ pointing to a file outside examples/
        # must be rejected and its target never read or printed.
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "secret.txt"
            outside.write_text("TOP SECRET\n")
            link = EXAMPLES / "tmp_escape_link.txt"
            self.assertFalse(link.exists())
            os.symlink(outside, link)
            try:
                p = run(["--read-example", "tmp_escape_link.txt"])
                self.assertNotEqual(p.returncode, 0)
                self.assertEqual(p.stdout, "")
            finally:
                link.unlink(missing_ok=True)

    def test_symlink_to_example_file_is_allowed(self):
        # A symlink inside examples/ that resolves to another file inside
        # examples/ is contained and may be read.
        link = EXAMPLES / "tmp_hello_link.txt"
        self.assertFalse(link.exists())
        os.symlink(EXAMPLES / "hello.txt", link)
        try:
            p = run(["--read-example", "tmp_hello_link.txt"])
            self.assertEqual(p.returncode, 0)
            self.assertEqual(p.stdout, "hello\n")
        finally:
            link.unlink(missing_ok=True)

    def test_missing_examples_dir_nonzero(self):
        # If examples/ were absent entirely, nothing could be read.
        # Simulate by pointing at a temp copy of the CLI whose examples/
        # root does not exist.
        with tempfile.TemporaryDirectory() as tmp:
            fake_root = Path(tmp) / "repo"
            fake_root.mkdir()
            shutil.copy2(CLI, fake_root / "sum-cli")
            p = subprocess.run(
                [sys.executable, str(fake_root / "sum-cli"),
                 "--read-example", "hello.txt"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(p.returncode, 0)
            self.assertEqual(p.stdout, "")

    def test_read_example_requires_path(self):
        self.assertNotEqual(run(["--read-example"]).returncode, 0)

    def test_read_example_extra_args_rejected(self):
        self.assertNotEqual(
            run(["--read-example", "hello.txt", "extra"]).returncode, 0
        )


class RegressionTest(unittest.TestCase):
    """Existing behavior must remain unchanged."""

    def test_valid_two_integers(self):
        self.assertEqual(run(["2", "3"]).stdout, "5\n")
        self.assertEqual(run(["-7", "10"]).stdout, "3\n")

    def test_no_arguments(self):
        self.assertNotEqual(run([]).returncode, 0)

    def test_one_argument(self):
        self.assertNotEqual(run(["1"]).returncode, 0)

    def test_three_arguments(self):
        self.assertNotEqual(run(["1", "2", "3"]).returncode, 0)

    def test_non_integer_alpha(self):
        self.assertNotEqual(run(["abc", "1"]).returncode, 0)

    def test_non_integer_float(self):
        self.assertNotEqual(run(["1.5", "2"]).returncode, 0)

    def test_version(self):
        p = run(["--version"])
        self.assertEqual(p.stdout, "sum-cli 1.0\n")
        self.assertEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main()
