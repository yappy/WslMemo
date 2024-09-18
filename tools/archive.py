#!/usr/bin/env python3

import argparse
import datetime
import getpass
import platform
import pathlib
import subprocess
import tempfile
import shutil

def exec(cmd: list[str]):
	print(f"EXEC: {' '.join(cmd)}")
	subprocess.run(cmd, check=True)

def archive(src: str, ar_dst: pathlib.Path, ext:str, parallel: bool):
	cwd = src.parent
	dir = src.name

	with tempfile.NamedTemporaryFile(suffix=f".{ext}") as tf:
		print(f"Temp file created: {tf.name}")
		# -C: change to directory DIR
		# -c: Create new.
		# -f: Specify file name.
		cmd = ["tar", "-C", str(cwd), "-cf", tf.name]
		if parallel:
			suffix = ar_dst.suffix
			if suffix == ".gz":
				cmd += ["--use-compress-prog=pigz"]
			elif suffix == ".bz2":
				cmd += ["--use-compress-prog=pbzip2"]
			elif suffix == ".xz":
				cmd += ["--use-compress-prog=xz -T 0"]
			else:
				assert False, "Specify .gz or .bz2 or .xz"
		else:
			# -a: Use archive suffix to determine the compression program.
			cmd += ["-a"]
		# source
		cmd.append(dir)

		print(f"Work Dir: {cwd}")
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
	parser.add_argument("--ext", "-e", default="tar.gz", help="compress file extention (e.g. tar.gz, tar.bz2, tar.xz)")
	parser.add_argument("--parallel", "-p", action="store_true", default=False, help="Parallel compression")
	args = parser.parse_args()

	user = getpass.getuser()
	host = platform.node()
	dt_now = datetime.datetime.now()
	dt_str = dt_now.strftime('%Y%m%d%H%M')

	src = pathlib.Path(args.src).resolve()
	assert src.is_dir(), "<src> must be a directory"
	dst = pathlib.Path(args.dst).resolve()
	dst.mkdir(parents=True, exist_ok=True)
	print(f"mkdir: {dst}")
	ar_dst = dst / f"{user}_{host}_{dt_str}.{args.ext}"
	print(f"SRC: {src}")
	print(f"DST: {ar_dst}")
	print()

	archive(src, ar_dst, args.ext, args.parallel)

	print("OK!")

if __name__ == '__main__':
	main()
