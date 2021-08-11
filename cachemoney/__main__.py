import argparse
import fnmatch
import os
import re
from urllib.parse import urlparse

from cachemoney.simplefile import parse_simplefile


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-dir", "-i", required=True)
    ap.add_argument("--output-root", "-o", help="output root directory")
    ap.add_argument("--filter", "-f", help="filter wildcard pattern (e.g. *jpg)")
    args = ap.parse_args()
    output_root = args.output_root
    cache_files = [
        os.path.join(args.cache_dir, filename)
        for filename in os.listdir(args.cache_dir)
        if re.match("^[0-9a-f]+_0$", filename)
    ]
    for file in cache_files:
        with open(file, "rb") as f:
            key, data = parse_simplefile(f)
        if args.filter and not fnmatch.fnmatch(key, args.filter):
            continue
        print(key)
        if output_root:
            url = urlparse(key)
            output_path = os.path.join(output_root, url.netloc, url.path.lstrip("/"))
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as outf:
                outf.write(data)
            print(" -> ", output_path)
            stat = os.stat(file)
            os.utime(output_path, (stat.st_atime, stat.st_mtime))


if __name__ == "__main__":
    main()
