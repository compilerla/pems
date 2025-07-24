import argparse
import sys

from pems_data.cache import Cache


def cache():  # prama: no cover
    parser = argparse.ArgumentParser("pems-cache", description="Simple CLI for the cache")
    parser.add_argument("op", choices=("check", "get", "set"), default="check", nargs="?", help="the operation to perform")
    parser.add_argument("--key", "-k", required=False, type=str, help="the item's key, required for get/set")
    parser.add_argument("--value", "-v", required=False, type=str, help="the item's value, required for set")
    parsed_args = parser.parse_args(sys.argv[1:])

    c = Cache()

    match parsed_args.op:
        case "get":
            if parsed_args.key:
                print(f"[{parsed_args.key}]: {c.get(parsed_args.key)}")
            else:
                parser.print_usage()
                raise SystemExit(1)
        case "set":
            if parsed_args.key and parsed_args.value:
                print(f"[{parsed_args.key}] = '{parsed_args.value}'")
                c.set(parsed_args.key, parsed_args.value)
            else:
                parser.print_usage()
                raise SystemExit(1)
        case _:
            print(f"cache is available: {c.is_available()}")
