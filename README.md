# paperclip-agent-acceptance

## sum-cli

Prints the arithmetic sum of exactly two base-10 integer arguments.

```sh
./sum-cli 2 3      # 5
./sum-cli -7 10    # 3
./sum-cli --version  # sum-cli 1.0
```

- Wrong argument count (anything other than exactly 2) exits non-zero.
- Non-integer arguments (e.g. `abc`, `1.5`) exit non-zero.
- `--version` prints `sum-cli 1.0` and exits 0.
- No stdin, other flags, or float support — integers only.

### Reading example files (`--read-example`)

```sh
./sum-cli --read-example hello.txt   # prints the contents of examples/hello.txt
```

`--read-example RELATIVE_PATH` prints the exact contents of a file from the
repository-local `examples/` directory (anchored at the directory containing
`sum-cli`, independent of the current working directory).

Constraints:

- Only relative paths are accepted; absolute paths exit non-zero.
- The path is fully resolved (following symlinks) against the real `examples/`
  root and must remain inside it — parent traversal (`../README.md`), deeper
  escapes (`subdir/../../README.md`), and symlinks pointing outside
  `examples/` all exit non-zero.
- The final target must be an existing regular file; missing files,
  directories, and non-regular files exit non-zero.
- Rejected targets are never read or printed — containment is validated
  before the file is opened.
- Nested relative paths inside `examples/` are supported (e.g.
  `sub/dir/file.txt`), as long as the resolved target stays inside
  `examples/`.
- A symlink inside `examples/` that resolves to another file inside
  `examples/` is allowed; one that escapes `examples/` is rejected.

### Tests

```sh
python3 tests/test_sum_cli.py
python3 tests/test_read_example.py
```
