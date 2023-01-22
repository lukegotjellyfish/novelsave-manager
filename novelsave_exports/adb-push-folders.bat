@ECHO OFF

:loop
rem python "C:\Users\Lukeg\Desktop\better-adb-sync-master\src\adbsync.py" --show-progress %1 "/storage/3934-3333/Lncrawl/novelsave/"
adb push --sync %1 "/storage/3934-3333/Lncrawl/novelsave/"
shift
if not "%~1"=="" goto loop

PAUSE