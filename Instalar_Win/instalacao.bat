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

set "PYDIR=%LocalAppData%\Programs\Python\Python311"
set "PYEXE=%PYDIR%\python.exe"
set "PYCMD="

REM 1) Ja existe um Python utilizavel neste computador?
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
echo (nao precisa clicar em nada, isso e automatico)
echo.

start /wait "" "%~dp0python-3.11.0-amd64.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1 Include_test=0 TargetDir="%PYDIR%"

if exist "%PYEXE%" (
    echo Python instalado com sucesso!
    set "PYCMD=%PYEXE%"
    goto :install_packages
)

REM 2) A instalacao automatica nao funcionou: tenta de novo, mas agora
REM    mostrando a tela do instalador, com instrucoes de como proceder.
echo.
echo Nao foi possivel instalar o Python automaticamente.
echo Vamos abrir a tela de instalacao do Python. Quando ela aparecer:
echo   1. Marque a caixinha "Add python.exe to PATH" (bem embaixo)
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
echo Depois, rode este arquivo (instalacao.bat) de novo.
echo.
pause
exit /b 1

:install_packages
echo.
echo Instalando as bibliotecas necessarias (numpy, pygame, pandas,
echo opencv-python)...
echo Isso tambem pode levar alguns minutos.
echo.

"%PYCMD%" -m pip install --upgrade pip
"%PYCMD%" -m pip install numpy pygame pandas opencv-python

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Algo deu errado ao instalar as bibliotecas.
    echo Verifique sua conexao com a internet e rode este arquivo de novo.
    echo Se o problema continuar, tire um print desta janela e envie
    echo para o suporte.
    echo.
    pause
    exit /b 1
)

echo.
echo Conferindo se esta tudo certo...
"%PYCMD%" -c "import numpy, pygame, pandas, tkinter, cv2" >nul 2>nul

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] A instalacao nao terminou corretamente.
    echo Rode este arquivo (instalacao.bat) de novo. Se o erro continuar,
    echo tire um print desta janela e envie para o suporte.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Instalacao concluida com sucesso!
echo.
echo   Agora voce pode fechar esta janela e abrir qualquer tarefa
echo   clicando duas vezes no arquivo "Executable.bat" dentro da
echo   pasta dela (ex: Tarefas\Abstract_Shapes\two_shapes).
echo ============================================================
echo.
pause
