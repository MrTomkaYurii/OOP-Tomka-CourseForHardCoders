# Генерація + експорт + перевірки всіх схем (або переданих): .\make.ps1 [назва ...] [--publish]
Push-Location $PSScriptRoot
try { python -m generator @args; exit $LASTEXITCODE } finally { Pop-Location }
