import argparse
import ctypes
import os
import platform
import glob
import tempfile
import subprocess


def command_search(args: argparse.Namespace):
	# Default to %LocalAppData%
	dir = args.dir if args.dir else os.getenv("LocalAppData")
	print(f"Searching for ext4.vhdx: {dir}")

	count = 0
	for name in glob.iglob(f"{dir}/**/ext4.vhdx", recursive=True):
		count += 1
		print(f"[{count}]")
		print(name)
		size, unit = auto_unit(os.path.getsize(name))
		print(f"Size: {size:.1f} {unit}B")
	print()
	print(f"{count} files found")


def command_compact(args: argparse.Namespace):
	file = args.VHDX
	print(f"Compacting: {file}")

	size, unit = auto_unit(os.path.getsize(file))
	print(f"Size: {size:.1f} {unit}B")
	print()

	check_env(require_admin=True)

	exec(["wsl", "--shutdown"])
	print("OK")
	print()

	with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
		print(f'select vdisk file="{file}"', file=f)
		print("attach vdisk readonly", file=f)
		print("compact vdisk", file=f)
		print("detach vdisk", file=f)

		f.seek(0)
		print("[Temporary Script]")
		print(f.read())

	# Windows requires releasing write lock
	try:
		exec(["diskpart.exe", "/s", f.name])
	finally:
		os.unlink(f.name)

	size2, unit2 = auto_unit(os.path.getsize(file))
	print(f"Original  Size: {size:.1f} {unit}B")
	print(f"Compacted Size: {size2:.1f} {unit2}B")


def check_env(*, require_admin: bool):
	if platform.system() != "Windows":
		raise RuntimeError("This script is Windows only")
	if require_admin and not ctypes.windll.shell32.IsUserAnAdmin():
		raise RuntimeError("This script requires admin rights")


def exec(cmd: list[str]):
	print(f"EXEC: {' '.join(cmd)}")
	subprocess.run(cmd, check=True)


def auto_unit(size: int) -> tuple[float, str]:
	size /= 1
	if size < 1024:
		return size, ""
	size /= 1024
	if size < 1024:
		return size, "Ki"
	size /= 1024
	if size < 1024:
		return size, "Mi"
	size /= 1024
	if size < 1024:
		return size, "Gi"
	size /= 1024
	return size, "Ti"


def main():
	check_env(require_admin=False)

	parser = argparse.ArgumentParser(description="WSL2 VHDX (virtual disk) utility")
	subparsers = parser.add_subparsers()

	parser_add = subparsers.add_parser("find", help="Search for VHDX files")
	parser_add.add_argument("--dir", help="Directory to search (default to %%LocalAppData%%)")
	parser_add.set_defaults(handler=command_search)

	parser_add = subparsers.add_parser("compact", help="Compact VHDX file")
	parser_add.add_argument("VHDX", help="VHDX file to be compacted")
	parser_add.set_defaults(handler=command_compact)

	args = parser.parse_args()
	if hasattr(args, "handler"):
		args.handler(args)
	else:
		parser.print_help()

if __name__ == "__main__":
	main()
