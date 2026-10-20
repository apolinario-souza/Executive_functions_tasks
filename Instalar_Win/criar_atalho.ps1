# Cria o ícone "Bateria de Funções Executivas" na área de trabalho e no
# menu Iniciar. Chamado pelo instalacao.bat, que passa o pythonw.exe (abre
# o programa sem a janela preta); descobre sozinho a pasta do programa (a
# pasta acima desta), então funciona com qualquer caminho.
param([Parameter(Mandatory = $true)][string]$PythonW)
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$battery = Join-Path $root 'Tarefas\Battery'
$main = Join-Path $battery 'main.py'
$icon = Join-Path $battery 'icone.ico'
$name = 'Bateria de Funções Executivas.lnk'

$shell = New-Object -ComObject WScript.Shell
foreach ($folder in @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('Programs'))) {
    $link = $shell.CreateShortcut((Join-Path $folder $name))
    $link.TargetPath = $PythonW
    $link.Arguments = '"' + $main + '"'
    $link.WorkingDirectory = $battery
    $link.IconLocation = $icon
    $link.Description = 'Tarefas computadorizadas de funções executivas'
    $link.Save()
}
