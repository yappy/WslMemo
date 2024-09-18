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

def robocopy(src_dir, dst_dir, ex_dirs, id, dry_run):
	if dst_dir.is_relative_to(src_dir):
		raise RuntimeError(f"{src_dir} is parent of {dst_dir}")

	log_file = dst_dir / f"{id}.txt"
	nproc = max(multiprocessing.cpu_count(), 128)
	cmd = [
		"Robocopy.exe", str(src_dir), str(dst_dir / src_dir.parts[-1]),
		# log
		f"/LOG:{log_file}",
		# No progress
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
	if ex_dirs:
		cmd += ["/XD"]
		cmd += ex_dirs
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
	parser.add_argument("--exclude-dir", action="append", default=[], help="exclude dir pattern")
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

	robocopy(src, dst, args.exclude_dir, id, args.dry_run)
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

'''

-------------------------------------------------------------------------------
   ROBOCOPY     ::     Windows の堅牢性の高いファイル コピー
-------------------------------------------------------------------------------

  開始: 2024年4月11日 9:45:34
              使用法:: ROBOCOPY コピー元 コピー先 [ファイル [ファイル]...]

                       [オプション]

           コピー元 :: コピー元ディレクトリ (ドライブ:\パスまたは \\サーバー

                       \共有\パス)。
           コピー先 :: コピー先ディレクトリ (ドライブ:\パスまたは \\サーバー

                       \共有\パス)。
           ファイル :: コピーするファイル (名前/ワイルドカード: 既定値は「*.*」

                       です)

::
:: コピー オプション:
::
                 /S :: サブディレクトリをコピーしますが、空のディレクトリはコピ

                       ーしません。
                 /E :: 空のディレクトリを含むサブディレクトリをコピーします。
             /LEV:n :: コピー元ディレクトリ ツリーの上位 n レベルのみをコピーし

                       ます。

                 /Z :: 再起動可能モードでファイルをコピーします。
                 /B :: バックアップ モードでファイルをコピーします。
                /ZB :: 再起動可能モードを使用します。アクセスが拒否された場合、

                       バックアップ モードを使用します。
                 /J :: バッファーなし I/O を使用してコピーします (大きなファイル

                       で推奨)。
            /EFSRAW :: 暗号化されたすべてのファイルを EFS RAW モードでコピーし

                       ます。

 /COPY:コピーフラグ :: ファイルにコピーする情報 (既定値は /COPY:DAT)。
                       (copyflags : D=データ、A=属性、T=タイムスタンプ、X=代替データ ストリームをスキップ)。
                       (S= セキュリティ =NTFS ACL、O= 所有者情報、U= 監査情報)。


               /SEC :: セキュリティと共にファイルをコピーします (/COPY:DATS と

                       同等)。
           /COPYALL :: ファイル情報をすべてコピーします (/COPY:DATSOU と同等)。
            /NOCOPY :: ファイル情報をコピーしません (/PURGE と共に使用すると便

                       利)。
            /SECFIX :: スキップしたファイルも含むすべてのファイルのファイル セ

                       キュリティを修正します。
            /TIMFIX :: スキップしたファイルも含むすべてのファイルのファイル時刻

                       を修正します。


             /PURGE :: 既にコピー元に存在しないコピー先のファイル/ディレクトリ

                       を削除します。
               /MIR :: ディレクトリ ツリーをミラー化します (/E および /PURGE と

                       同等)。

               /MOV :: ファイルを移動します (コピー後にコピー元から削除)。
              /MOVE :: ファイルとディレクトリを移動します (コピー後にコピー元か

                       ら削除)。

     /A+:[RASHCNET] :: コピーされたファイルに指定の属性を追加します。
     /A-:[RASHCNET] :: コピーされたファイルから指定の属性を削除します。

            /CREATE :: ディレクトリ ツリーと長さ 0 のファイルのみを作成します。
               /FAT :: 8.3 FAT ファイル名のみを使用してコピー先ファイルを作成し

                       ます。
               /256 :: 256 文字を超える非常に長いパスのサポートをオフにします。

             /MON:n :: コピー元を監視し、n 回を超える変更があった場合に再度実行

                       します。
             /MOT:m :: コピー元を監視し、m 分後に変更があった場合に再度実行

                       します。

      /RH:hhmm-hhmm :: 実行時間 - 新しいコピーを開始できる時刻です。
                /PF :: 実行時間をファイルごと (パスごとではない) に確認します。

             /IPG:n :: 低速回線で帯域幅を解放するためのパケット間ギャップ (ミリ

                       秒)。

                /SJ :: 接合のターゲットとしてではなく接合として Junctions をコピーします。
                /SL:: リンクのターゲットとしてではなくリンクとしてシンボリック リンクをコピーします。

            /MT[:n] :: n 個のスレッドのマルチスレッド コピーを実行します (既定値 8)。
                       n は 1 から 128 までの値である必要があります。
                       このオプションは、/IPG および /EFSRAW オプションと互換性がありません。
                       パフォーマンス向上のため、/LOG オプションを使用して出力をリダイレクトします。

/DCOPY:コピーフラグ :: ディレクトリにコピーする情報 (既定値は /DCOPY:DA)。
                       (copyflags : D=データ、A=属性、T=タイムスタンプ、E=EA、X=代替データ ストリームをスキップ)。

           /NODCOPY :: ディレクトリ情報をコピーしません (既定では /DCOPY:DA が実行されます)。

         /NOOFFLOAD :: Windows のオフロードをコピーするメカニズムを使用せずに、

                       ファイルをコピーします。

          /COMPRESS :: ファイル転送中にネットワーク圧縮を要求します (適用可能な場合)。

::
:: ファイル選択オプション:
::
                 /A :: アーカイブ属性が設定されているファイルのみをコピーしま

                       す。
                 /M :: アーカイブ属性のあるファイルのみをコピーし、リセットしま

                       す。
    /IA:[RASHCNETO] :: 指定されたいずれかの属性が設定されているファイルのみを含

                       みます。
    /XA:[RASHCNETO] :: 指定されたいずれかの属性が設定されているファイルを除外し

                       ます。

/XF file [ファイル]... ::

                       指定された名前/パス/ワイルドカードに一致するファイルを

                       除外します。
/XD dir [ディレクトリ]... ::

                       指定された名前/パスに一致するディレクトリを除外します。

                /XC :: 変更されたファイルを除外します。
                /XN :: 新しいファイルを除外します。
                /XO :: 古いファイルを除外します。
                /XX :: コピー先にだけ存在するファイルとディレクトリを除外し

                       ます。
                /XL :: コピー元にだけ存在するファイルとディレクトリを除外し

                       ます。
                /IS :: 同一ファイルを含みます。
                /IT :: 異常なファイルを含めます。

             /MAX:n :: 最大ファイル サイズ - n バイトより大きいファイルを除外し

                       ます。
             /MIN:n :: 最小ファイル サイズ - n バイトより小さいファイルを除外し

                       ます。

          /MAXAGE:n :: 最長ファイル有効期間 - n 日より古いファイルを除外します。
          /MINAGE:n :: 最短ファイル有効期間 - n 日より新しいファイルを除外しま

                       す。
          /MAXLAD:n :: 最大最終アクセス日 - n で指定する値以後に使用していない

                       ファイルを除外します。
          /MINLAD:n :: 最小最終アクセス日 - n で指定する値以後に使用されたファ

                       イルを除外します。
                       (n < 1900 の場合、n = n 日です。それ以外は、n = YYYYMMDD

                       の日付です)。

               /FFT :: FAT ファイル時間 (2 秒の粒度) を想定します。
               /DST :: 1 時間の DST 時間差を補正します。

                /XJ:: シンボリック リンク (ファイルとディレクトリの両方) と接合ポイントを除外します。
               /XJD:: ディレクトリのシンボリック リンクと接合ポイントを除外します。
               /XJF :: ファイルのシンボリック リンクを除外します。

                /IM :: 変更されたファイルを含めます (変更日時が異なる)。
::
:: 再試行オプション:
::
               /R:n :: 失敗したコピーに対する再試行数: 既定値は 1,000,000。
               /W:n :: 再試行と再試行の間の待機時間: 既定値は、30 秒です。

               /REG :: /既定の設定としてレジストリに R:n と /W:n を保存します。

               /TBD :: 共有名が定義されるのを待ちます (再試行エラー 67)。

               /LFSM :: 空き領域不足モードで動作し、コピーの一時停止と再開を有効にします (「注釈」を参照)。

               /LFSM:n[KMG] :: 下限サイズを n [K:kilo,M:mega,G:giga] バイトで指定した /LFSM。

::
:: ログ オプション:
::
                 /L :: リストのみ - いずれのファイルにも、コピー、タイムスタン

                       プの追加、または削除を実施しません。
                 /X :: 選択されたファイルのみではなく、余分なファイルをすべて報

                       告します。
                 /V :: スキップされたファイルを示す詳細出力を作成します。
                /TS :: 出力にコピー元ファイルのタイム スタンプを含めます。
                /FP :: 出力にファイルの完全なパス名を含めます。
             /BYTES :: サイズをバイトで出力します。

                /NS :: サイズなし - ファイル サイズをログに記録しません。
                /NC :: クラスなし - ファイル クラスをログに記録しません。
               /NFL :: ファイル リストなし - ファイル名をログに記録しません。
               /NDL :: ディレクトリなし - ディレクトリ名をログに記録しません。

                /NP :: 進行状況なし - コピーの完了率を表示しません。
               /ETA :: コピーするファイルの推定完了時刻を表示します。

      /LOG:ファイル :: ログ ファイルに状態を出力します (既存のログを上書きしま

                       す)。
     /LOG+:ファイル :: ログ ファイルに状態を出力します (既存のログ ファイルに

                       追加します)。

   /UNILOG:ファイル :: ログ ファイルに UNICODE で状態を出力します (既存のログを

                       上書きします)。
  /UNILOG+:ファイル :: ログ ファイルに UNICODE で状態を出力します (既存のログに

                       追加します)。

               /TEE :: コンソール ウィンドウとログ ファイルに出力します。

               /NJH :: ジョブ ヘッダーがありません。
               /NJS :: ジョブ要約がありません。

           /UNICODE :: 状態を UNICODE で出力します。

::
:: ジョブ オプション:
::
      /JOB:ジョブ名 :: 名前の付いたジョブ ファイルからパラメーターを取得します。
     /SAVE:ジョブ名 :: 名前の付いたジョブ ファイルにパラメーターを保存します。
              /QUIT :: コマンド ラインの処理後に終了します (パラメーターの表示の

                       ため)。
              /NOSD :: コピー元ディレクトリを指定しません。
              /NODD :: コピー先ディレクトリを指定しません。
                /IF :: 後続のファイルを含みます。

::
:: 注釈 :
::
       ボリュームのルート ディレクトリに対して /PURGE または /MIR を使用すると、これまでは、
       robocopy は要求された操作をシステム ボリューム情報ディレクトリ内のファイル
       にも適用していました。この動作は変更されました。
       どちらかを指定すると、robocopy はその名前を持つファイルまたはディレクトリを
       (コピー セッションの最上位レベルのソースと宛先ディレクトリで) スキップします。

       変更されたファイルの分類は、コピー元とコピー先両方の
       ファイル システムが変更タイムスタンプ (NTFS など) をサポートしていて、
       コピー元とコピー先のファイルの変更日時が異なり、しかし
       それ以外は同じ場合に適用されます。これらのファイルは既定ではコピーされません。/IM を指定して、
       それらを含めます。

       /DCOPY:E フラグは、拡張属性コピーを
       ディレクトリに対して試行することを要求します。現時点では robocopy が継続されます
       (ディレクトリの EA をコピーできなかった場合)。このフラグは
       /COPYALL 内。

       /LFSM を使用することで、robocopy に '空き領域不足モード' での動作を要求します。
       そのモードでは、次の場合に robocopy が一時停止します。すなわち、ファイルのコピーによって
       コピー先ボリュームの空き領域が '下限' 値を下回る場合です。この値は
       フラグの LFSM:n[KMG] 形式によって明示的に指定できます。
       /LFSM が明示的な下限値なしで指定されている場合、下限は
       コピー先ボリュームのサイズの 10% に設定されます。
       空き領域不足モードは、/MT、/EFSRAW、/B、および/ZB と互換性がありません。
'''
