# paperclip-agent-acceptance

## sum-cli

A small CLI that sums numbers.

```sh
./sum-cli 1 2 3        # 6
./sum-cli 1.5 2.5      # 4.0
echo "1\n2" | ./sum-cli  # 6  (reads numbers from stdin when no args are given)
```

Invalid input exits with status 1 and an error on stderr.

### Tests

```sh
python3 tests/test_sum_cli.py
```