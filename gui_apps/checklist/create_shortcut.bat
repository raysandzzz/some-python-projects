@echo off
set SCRIPT_DIR=%~dp0
set TARGET=%SCRIPT_DIR%checklist_main.pyw
set ICON=%SCRIPT_DIR%icon.ico
set SHORTCUT=%USERPROFILE%\Desktop\Checklist.lnk

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = 'pythonw.exe'; $s.Arguments = '\"%TARGET%\"'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.IconLocation = '%ICON%'; $s.Save()"

echo Shortcut created succesfully on your desktop! :D
pause