@echo off

rem check command line parameter
if "%~1"=="" (
	echo Usage: %0 VHDX_FILE
	exit /b 1
)

rem run as administrator if not
whoami /priv | find "SeDebugPrivilege" > nul
if %errorlevel% neq 0 (
	@powershell start-process "%~0" "%~1" -verb runas
	exit
)

set SCRIPT=diskpart_script.txt
echo VHDX_FILE: %~1
set ORG_SIZE=%~z1
call :ShowFileSize %ORG_SIZE%
echo;

echo wsl shutdown
wsl --shutdown
echo OK
echo;

echo [%SCRIPT%]
echo select vdisk file="%~1"> %SCRIPT%
echo attach vdisk readonly>> %SCRIPT%
echo compact vdisk>> %SCRIPT%
echo detach vdisk>> %SCRIPT%
type %SCRIPT%
echo;

echo diskpart /s %SCRIPT%
diskpart /s %SCRIPT%

pause
goto :EOF


:ShowFileSize
set BSIZE=%1
set KSIZE=%BSIZE:~0,-3%
set MSIZE=%KSIZE:~0,-3%
set GSIZE=%MSIZE:~0,-3%
set TSIZE=%GSIZE:~0,-3%

if not "%TSIZE%"=="" (
	echo %TSIZE% TB
) else if not "%GSIZE%"=="" (
	echo %GSIZE% GB
) else if not "%MSIZE%"=="" (
	echo %MSIZE% MB
) else if not "%KSIZE%"=="" (
	echo %KSIZE% KB
) else (
	echo %BSIZE% B
)

exit /b
