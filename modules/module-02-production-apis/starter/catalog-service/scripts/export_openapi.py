import argparse
import json
import sys
from urllib.request import urlopen


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True, help="Example: http://localhost:8000")
    parser.add_argument("--out", required=True, help="Output file path")
    args = parser.parse_args()

    url = args.base_url.rstrip("/") + "/openapi.json"
    with urlopen(url) as resp:  # noqa: S310 - used for local lab tooling
        spec = json.loads(resp.read().decode("utf-8"))

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


