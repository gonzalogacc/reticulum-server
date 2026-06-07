
# reticulum-server

This is to generate a fixed destination to use with the server

```bash
# Generate an identity to use here 
uv run rnid -g ./test-server

# Set that identity in the configuration
```

Run the server

```bash
make run
```

From another conosle maque a request

```bash
uv run python ret_curl.py b1eea1ed49cb50700443d4f7148fd6ed /random/text --payload '{"some": "payload", "another": "nono"}' --config ~/.reticulum
```
