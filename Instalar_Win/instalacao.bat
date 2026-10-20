@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

title Instalacao - Bateria de Funcoes Executivas

echo ============================================================
echo   Instalando os programas necessarios para rodar as tarefas
echo ============================================================
echo.
echo Esta janela vai ficar aberta o tempo todo. Nao feche ate
echo aparecer a mensagem "Instalacao concluida com sucesso!".
echo.

for %%i in ("%~dp0..") do set "ROOT=%%~fi"
set "PYDIR=%LocalAppData%\Programs\Python\Python311"
set "PYEXE=%PYDIR%\python.exe"
set "PYCMD="

REM ------------------------------------------------------------
REM 1) Python: usa o que ja existe ou instala o que vem nesta pasta
REM ------------------------------------------------------------
where py >nul 2>nul
if %errorlevel%==0 (
    echo Python ja esta instalado neste computador. Pulando essa etapa.
    set "PYCMD=py"
    goto :install_packages
)

if exist "%PYEXE%" (
    echo Python ja foi instalado anteriormente. Pulando essa etapa.
    set "PYCMD=%PYEXE%"
    goto :install_packages
)

echo Instalando o Python agora, isso pode levar alguns minutos...
echo - nao precisa clicar em nada, isso e automatico -
echo.

start /wait "" "%~dp0python-3.11.0-amd64.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1 Include_test=0 TargetDir="%PYDIR%"

if exist "%PYEXE%" (
    echo Python instalado com sucesso!
    set "PYCMD=%PYEXE%"
    goto :install_packages
)

REM A instalacao automatica nao funcionou: tenta de novo, mas agora
REM mostrando a tela do instalador, com instrucoes de como proceder.
echo.
echo Nao foi possivel instalar o Python automaticamente.
echo Vamos abrir a tela de instalacao do Python. Quando ela aparecer:
echo   1. Marque a caixinha "Add python.exe to PATH" - bem embaixo
echo   2. Clique em "Install Now"
echo   3. Espere terminar e feche a janela do instalador
echo.
pause
start /wait "" "%~dp0python-3.11.0-amd64.exe"

where py >nul 2>nul
if %errorlevel%==0 (
    set "PYCMD=py"
    goto :install_packages
)

echo.
echo [ERRO] O Python ainda nao foi encontrado neste computador.
echo Tente instalar manualmente clicando duas vezes em:
echo    python-3.11.0-amd64.exe
echo E marque a opcao "Add python.exe to PATH" durante a instalacao.
echo Depois, rode este arquivo instalacao.bat de novo.
echo.
pause
exit /b 1

REM ------------------------------------------------------------
REM 2) Bibliotecas usadas pelas tarefas e pela planilha de resultados
REM ------------------------------------------------------------
:install_packages
echo.
echo Instalando as bibliotecas necessarias: numpy, pygame, pandas e openpyxl.
echo Isso tambem pode levar alguns minutos.
echo.

"%PYCMD%" -m pip install --upgrade pip
"%PYCMD%" -m pip install numpy pygame pandas openpyxl

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Algo deu errado ao instalar as bibliotecas.
    echo Verifique sua conexao com a internet e rode este arquivo de novo.
    echo Se o problema continuar, tire um print desta janela e envie
    echo para o suporte: edf.tercio@gmail.com
    echo.
    pause
    exit /b 1
)

echo.
echo Conferindo se esta tudo certo...
"%PYCMD%" -c "import numpy, pygame, pandas, openpyxl, tkinter" >nul 2>nul

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] A instalacao nao terminou corretamente.
    echo Rode este arquivo instalacao.bat de novo. Se o erro continuar,
    echo tire um print desta janela e envie para o suporte: edf.tercio@gmail.com
    echo.
    pause
    exit /b 1
)

REM ------------------------------------------------------------
REM 3) Icone na area de trabalho e no menu Iniciar
REM ------------------------------------------------------------
REM pythonw.exe abre o programa sem a janela preta
for /f "usebackq delims=" %%i in (`"%PYCMD%" -c "import os, sys; print(os.path.join(os.path.dirname(sys.executable), 'pythonw.exe'))"`) do set "PYW=%%i"

echo.
echo Criando o icone na area de trabalho...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0criar_atalho.ps1" -PythonW "%PYW%"

if %errorlevel% neq 0 (
    echo.
    echo [AVISO] Nao foi possivel criar o icone na area de trabalho.
    echo O programa foi instalado: para abrir, de dois cliques em
    echo INICIAR_BATERIA.bat, na pasta do programa.
    echo.
)

echo.
echo ============================================================
echo   Instalacao concluida com sucesso!
echo.
echo   Para abrir o programa, de dois cliques no icone
echo   "Bateria de Funcoes Executivas" na area de trabalho.
echo.
echo   Aperte qualquer tecla para abrir o programa agora.
echo ============================================================
echo.
pause >nul
start "" "%PYW%" "%ROOT%\Tarefas\Battery\main.py"
