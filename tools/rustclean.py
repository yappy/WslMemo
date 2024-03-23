#!/usr/bin/env python3

import argparse
import pathlib
import subprocess

def clean_all(root):
	for p in pathlib.Path(root).glob("**/Cargo.toml"):
		dir = p.parent
		if all((not p.name.startswith(".") for p in dir.parents)):
			print(dir)
			subprocess.run(["cargo", "clean"], cwd=dir, check=True)

def main():
	parser = argparse.ArgumentParser(description="cargo clean in all directories")
	parser.add_argument("root", help="root dir")
	args = parser.parse_args()

	clean_all(args.root)

if __name__ == '__main__':
	main()
