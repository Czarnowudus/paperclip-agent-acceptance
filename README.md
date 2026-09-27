# paperclip-agent-acceptance

## sum-cli

Prints the arithmetic sum of exactly two base-10 integer arguments.

```sh
./sum-cli 2 3      # 5
./sum-cli -7 10    # 3
```

- Wrong argument count (anything other than exactly 2) exits non-zero.
- Non-integer arguments (e.g. `abc`, `1.5`) exit non-zero.
- No stdin, flags, or float support — integers only.

### Tests

```sh
python3 tests/test_sum_cli.py
```
