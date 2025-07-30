# `pems-cache` CLI

The `pems_data` package includes `pems-cache`, a simple command-line tool for interacting directly with the Redis cache. It's useful for debugging cache issues or manually inspecting and setting values.

## Commands

The CLI supports three main operations:

- `check`
- `get`
- `set`

If you run `pems-cache` with no operation, it defaults to `check`.

### `check`

Verifies that a connection to the Redis server can be established and that the cache is responsive.

#### Usage

```shell
pems-cache check
```

#### Example output

```shell
$ pems-cache check
cache is available: True
```

### `get`

Retrieves and displays a value from the cache based on its key. The `--key` (or `-k`) argument is required.

#### Usage

```shell
pems-cache get --key <cache-key>
```

#### Example output

```shell
$ pems-cache get --key "stations:metadata:district:7"
[stations:metadata:district:7]: b'\x01\x00\x00\x00\xff\xff...'
```

### `set`

Sets a string value for a given key in the cache. Both the `--key` (`-k`) and `--value` (`-v`) arguments are required.

#### Usage

```shell
pems-cache set --key <cache-key> --value <cache-value>
```

#### Example output

```shell
$ pems-cache set -k "my:test:key" -v "hello from the cli"
[my:test:key] = 'hello from the cli'
```
