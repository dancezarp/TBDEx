@echo off
set arg1=%1
set arg2=%2
set arg3=%3
set arg4=%4
set arg5=%5
powershell.exe -executionpolicy bypass -File "l.ps1" %arg1% %arg2% %arg3% %arg4% %arg5%