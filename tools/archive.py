#!/usr/bin/env python3

import argparse
import datetime
import getpass
import platform
import pathlib
import subprocess
import tempfile
import shutil

def exec(cmd):
	print(f"EXEC: {cmd}")
	subprocess.run(cmd, check=True)

def archive(src, ar_dst):
	cwd = src.parent
	dir = src.name

	with tempfile.NamedTemporaryFile() as tf:
		print(f"Temp file created: {tf.name}")
		# -a: Use archive suffix to determine the compression program.
		# -c: Create new.
		# -f: Specify file name.
		cmd = ["tar", "-C", str(cwd), "-acf", tf.name, dir]
		exec(cmd)
		print()

		print(f"Copy {tf.name} -> {ar_dst}")
		shutil.copyfile(tf.name, str(ar_dst))
		print(f"Delete temp file: {tf.name}")
		# close and delete

def main():
	parser = argparse.ArgumentParser(description="Archive and compress directory")
	parser.add_argument("src", help="backup source root (e.g. ~)")
	parser.add_argument("dst", help="backup destination root (e.g. /mnt/d)")
	parser.add_argument("--ext", default="tar.gz", help="compress file extention (e.g. tar.gz, tar.bz2, tar.xz)")
	args = parser.parse_args()

	user = getpass.getuser()
	host = platform.node()
	dt_now = datetime.datetime.now()
	dt_str = dt_now.strftime('%Y%m%d_%H%M')

	src = pathlib.Path(args.src).resolve()
	assert src.is_dir(), "<src> must be a directory"
	dst = pathlib.Path(args.dst).resolve()
	ar_dst = dst / f"{user}_{host}_{dt_str}.{args.ext}"
	print(f"SRC: {src}")
	print(f"DST: {ar_dst}")
	print()

	dst.mkdir(parents=True, exist_ok=True)
	print(f"mkdir: {dst}")
	archive(src, ar_dst)

	print("OK!")

if __name__ == '__main__':
	main()
