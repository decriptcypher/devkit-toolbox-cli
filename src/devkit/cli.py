import argparse

from devkit.crypto import hash


def main() -> None:
    parser = argparse.ArgumentParser(prog="devkit")
    subparsers = parser.add_subparsers(dest="command")

    hash_parser = subparsers.add_parser("hash", help="Generate a hash for a file or text")
    hash_parser.add_argument("value", help="File path (default) or text (with --text)")
    hash_parser.add_argument(
        "--text", action="store_true", help="Treat 'value' as literal text instead of a file path"
    )
    hash_parser.add_argument(
        "--algo", choices=["md5", "sha1", "sha256"], default="sha256", help="Hash algorithm (default: sha256)"
    )

    args = parser.parse_args()

    if args.command == "hash":
        hash.run(args.value, algo=args.algo, as_text=args.text)
