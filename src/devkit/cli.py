import argparse

from devkit.crypto import hash
from devkit.files import diskreport


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

    diskreport_parser = subparsers.add_parser(
        "diskreport", help="Report the largest or oldest/newest files in a directory"
    )
    diskreport_parser.add_argument(
        "path", nargs="?", default=".", help="Directory to scan (default: current directory)"
    )
    diskreport_parser.add_argument(
        "--by", choices=["size", "age"], default="size", help="Sort by size or last modified time (default: size)"
    )
    diskreport_parser.add_argument(
        "--order",
        choices=["desc", "asc"],
        default="desc",
        help="desc = largest/oldest first, asc = smallest/newest first (default: desc)",
    )
    diskreport_parser.add_argument("--top", type=int, default=10, help="Number of results to show (default: 10)")

    args = parser.parse_args()

    if args.command == "hash":
        hash.run(args.value, algo=args.algo, as_text=args.text)
    elif args.command == "diskreport":
        diskreport.run(args.path, by=args.by, order=args.order, top=args.top)
