# src/gitlater/cli.py

import sys

from gitlater.core import check_allowed, get_status


def main() -> None:
    args = sys.argv[1:]

    if not args:
        print("gitlater: missing command")
        print("Usage: gitlater [check|status]")
        sys.exit(1)

    cmd = args[0]

    if cmd == "check":
        allowed, message = check_allowed()

        if not allowed:
            print(message)
            sys.exit(1)

        # silent success
        sys.exit(0)

    elif cmd == "status":
        print(get_status())
        sys.exit(0)

    else:
        print(f"gitlater: unknown command '{cmd}'")
        print("Usage: gitlater [check|status]")
        sys.exit(1)


if __name__ == "__main__":
    main()
