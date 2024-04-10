#!/usr/bin/env python3

import argparse
import datetime
import sys
import getpass
import platform
import pathlib
import subprocess
import shutil
import multiprocessing

def robocopy(src_dir, dst_dir, id, dry_run):
	if dst_dir.is_relative_to(src_dir):
		raise RuntimeError(f"{src_dir} is parent of {dst_dir}")

	log_file = dst_dir / f"{id}.txt"
	nproc = max(multiprocessing.cpu_count(), 128)
	cmd = [
		"Robocopy.exe", str(src_dir), str(dst_dir / src_dir.parts[-1]),
		# log
		f"/LOG:{log_file}",
		"/NP",
		# Mirror (files may be deleted!)
		"/MIR",
		# Copy timestamp
		"/COPY:DAT",
		"/DCOPY:DAT",
		# Exclude System, Hidden, Temp, Offline
		# Exclude link/junction
		"/XA:SHTO",
		"/XJ",
		# Multi-threading
		f"/MT:{nproc}",
		# Retry count and Wait sec
		"/R:1",
		"/W:0 ",
	]
	if dry_run:
		cmd += ["/L"]

	proc = subprocess.run(cmd, check=False)
	print()
	print(f"Robocopy returned: {proc.returncode}")
	print()

def archive(src_dir, ar_dst, dry_run):
	if ar_dst.is_relative_to(src_dir):
		raise RuntimeError(f"{src_dir} is parent of {ar_dst}")

	shutil.make_archive()

def win_main():
	parser = argparse.ArgumentParser(
		description="Archive and compress directory",
	)
	parser.add_argument("src", help="backup source dir (e.g. C/:Users/<user>)")
	parser.add_argument("dst", help="backup destination dir (e.g. D:/bkup)")
	parser.add_argument("-d", "--dry_run", action="store_true", help="dry run")
	args = parser.parse_args()

	host = platform.node()
	dt_now = datetime.datetime.now()
	dt_str = dt_now.strftime('%Y%m%d_%H%M')
	user = getpass.getuser()

	src = pathlib.Path(args.src).resolve()
	assert src.is_dir(), "<src> must be a directory"
	dst = pathlib.Path(args.dst).resolve()
	dst.mkdir(parents=True, exist_ok=True)
	print(f"mkdir: {dst}")
	assert dst.is_dir(), "<dst> must be a directory"
	id = f"{user}_{host}_{dt_str}"
	ar_dst = dst / f"{id}.zip"

	print(f"SRC: {src}")
	print(f"DST: {dst}")
	print()

	robocopy(src, dst, id, args.dry_run)
	#archive(src, ar_dst, args.dry_run)

def wsl_to_win(wslpath):
	proc = subprocess.run(
		["wslpath", "-w", str(wslpath)],
		check=True, text=True, stdout=subprocess.PIPE, stderr=None)
	return pathlib.PureWindowsPath(proc.stdout.strip())

def wsl_main():
	self_py = wsl_to_win(__file__)
	cmd = ["py.exe", "-3", str(self_py)] + sys.argv[1:]

	print("Execute Windows python...")
	print(f"Run: {' '.join(cmd)}")
	print("-" * 80)
	try:
		subprocess.run(cmd, check=True)
		print("-" * 80)
		print("Windows python exited successfully")
	except subprocess.CalledProcessError as e:
		print("-" * 80)
		print(f"Error: Windows python exited with exitcode={e.returncode}")
		print()
		raise
	except:
		print("-" * 80)
		print("Exec py.exe error:")
		print("Please confirm that Windows python (NOT a MS store version) is available.")
		print("Then it is needed to restart WSL.")
		print("> winget.exe search python.python")
		print("> winget.exe install Python.Python.3.x")
		print("> wsl.exe --shutdown")
		print()
		raise

def main():
	system = platform.system()
	if system == "Linux":
		wsl_main()
	elif system == "Windows":
		win_main()

if __name__ == '__main__':
	main()
