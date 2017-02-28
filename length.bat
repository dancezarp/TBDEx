@echo off
set arg1=%1
set arg2=%2
set arg3=%3
set arg4=%4
powershell.exe -executionpolicy bypass -File "s.ps1" %arg1% %arg2% %arg3% %arg4%