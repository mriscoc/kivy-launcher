Write-Host "🔍 Verificando versión de Python..."
$pythonVersion = & python --version 2>&1
if ($pythonVersion -notmatch "3\.\d+") {
    Write-Host "❌ Se requiere Python 3.x desde https://www.python.org"
    exit 1
}

$venvPath = ".\.venv"
if (Test-Path $venvPath) {
    Write-Host "✅ El entorno virtual ya existe en '$venvPath'. Usándolo directamente..."
} else {
    Write-Host "🐍 Creando entorno virtual..."
    & python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❗ Error al crear el entorno virtual."
        exit 1
    }
}

Write-Host "⚙️ Activando el entorno virtual..."
Set-ExecutionPolicy RemoteSigned -Scope Process -Force
. "$venvPath\Scripts\Activate.ps1"

Write-Host "📦 Actualizando pip..."
& python -m pip install --upgrade pip 2>&1 | ForEach-Object { Write-Host $_ }

Write-Host "📚 Instalando dependencias desde requirements.txt..."
& pip install -r requirements.txt 2>&1 | ForEach-Object { Write-Host $_ }

Write-Host "🚀 Entorno listo para trabajar." -ForegroundColor Green