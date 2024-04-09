#!/usr/bin/env python3

import argparse
import pathlib
import subprocess

CLEAN_PATTERN = [
	("make", "**/Makefile", ["make", "clean"]),
	("cargo", "**/Cargo.toml", ["cargo", "clean"]),
]

def clean_all(root, pat, cmd):
	for p in pathlib.Path(root).glob(pat):
		dir = p.parent
		# Ignore if under hidden directory (**/.*/**)
		if all((not p.name.startswith(".") for p in dir.parents)):
			print(" ".join(cmd))
			print(f"in {dir}")
			subprocess.run(cmd, cwd=dir, check=False)
			print()

def main():
	parser = argparse.ArgumentParser(description="Find build file and clean")
	for tag, pat, cmd in CLEAN_PATTERN:
		parser.add_argument(f"--{tag}", action="store_true", help=f"Find {pat} and `{' '.join(cmd)}`")
	parser.add_argument("root", help="root dir")
	args = vars(parser.parse_args())

	exec_any = False
	for tag, pat, cmd in CLEAN_PATTERN:
		if args[tag]:
			exec_any = True
			clean_all(args["root"], pat, cmd)
	if not exec_any:
		print("Specify at least one clean option.")
		print("-h or --help to show help.")

if __name__ == '__main__':
	main()
