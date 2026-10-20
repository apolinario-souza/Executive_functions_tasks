@echo off
REM Abre o menu da bateria sem a janela preta. Se o programa ainda nao foi
REM instalado, explica o que fazer.
cd /d "%~dp0Tarefas\Battery"

where pyw >nul 2>nul
if %errorlevel%==0 (
    start "" pyw main.py
    exit /b 0
)

if exist "%LocalAppData%\Programs\Python\Python311\pythonw.exe" (
    start "" "%LocalAppData%\Programs\Python\Python311\pythonw.exe" main.py
    exit /b 0
)

echo O programa ainda nao foi instalado neste computador.
echo Abra a pasta Instalar_Win e de dois cliques em instalacao.bat.
echo.
pause
