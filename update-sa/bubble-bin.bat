@echo off
setlocal

set BUBBLEDASH_PATH=%~dp0BubbleDash.py
set PORTWARN_PATH=%~dp0PWRN.py
set LOG_FILE=%~dp0startup_log.txt

set l=false

if /i "%l%"=="true" (
    echo %date% %time% >> "%LOG_FILE%"
)

python "%BUBBLEDASH_PATH%" > nul 2>&1
if %errorlevel% neq 0 (
    if /i "%l%"=="true" echo Erro ao iniciar BubbleDash.py. >> "%LOG_FILE%"
) else (
    if /i "%l%"=="true" echo BubbleDash.py iniciou com sucesso. >> "%LOG_FILE%"
)

python "%PORTWARN_PATH%" > nul 2>&1
if %errorlevel% neq 0 (
    if /i "%l%"=="true" echo Erro ao iniciar PortWarn.py. >> "%LOG_FILE%"
) else (
    if /i "%l%"=="true" echo PortWarn.py iniciou com sucesso. >> "%LOG_FILE%"
)

if /i "%l%"=="true" echo Script de inicialização concluído. >> "%LOG_FILE%"

endlocal