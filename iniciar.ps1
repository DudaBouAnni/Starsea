# Inicia a API com o banco do .env; migracoes remotas exigem opcao explicita.
param([switch]$AplicarMigracoes)

$ErrorActionPreference = 'Stop'
$projectDirectory = $PSScriptRoot
$pythonExecutable = Join-Path $projectDirectory '.venv\Scripts\python.exe'
$mysqlDirectory = Join-Path $projectDirectory '.runtime\mysql-local'
$mysqlConfiguration = Join-Path $mysqlDirectory 'my.ini'

function Test-LocalPort {
    param([int]$Port)
    $connection = New-Object System.Net.Sockets.TcpClient
    try {
        $attempt = $connection.ConnectAsync('127.0.0.1', $Port)
        return $attempt.Wait(500) -and $connection.Connected
    } catch {
        return $false
    } finally {
        $connection.Dispose()
    }
}

if (-not (Test-Path -LiteralPath $pythonExecutable)) {
    throw 'O ambiente Python .venv não foi encontrado. Instale as dependências primeiro.'
}

Push-Location -LiteralPath $projectDirectory
try {
    $databaseTargetJson = & $pythonExecutable -c 'import json; from app.database.session import engine, AUTO_CREATE_TABLES; print(json.dumps(dict(local=AUTO_CREATE_TABLES, backend=engine.dialect.name, port=engine.url.port or 3306)))'
    if ($LASTEXITCODE -ne 0) {
        throw 'Não foi possível carregar o .env ou o certificado definido em CA_PATH.'
    }
    $databaseTarget = $databaseTargetJson | ConvertFrom-Json
    if ($databaseTarget.local -and $databaseTarget.backend -eq 'mysql' -and -not (Test-LocalPort -Port $databaseTarget.port)) {
        if ($databaseTarget.port -ne 3306) {
            throw 'Inicie o MySQL local na porta configurada no .env.'
        }
        $mysqlPackage = Get-ChildItem -LiteralPath $mysqlDirectory -Directory -Filter 'mysql-*-winx64' -ErrorAction SilentlyContinue |
            Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'bin\mysqld.exe') } |
            Select-Object -First 1
        if (-not $mysqlPackage -or -not (Test-Path -LiteralPath $mysqlConfiguration)) {
            throw 'Inicie seu servidor MySQL na porta 3306; a instalação local não foi encontrada.'
        }
        $mysqlExecutable = Join-Path $mysqlPackage.FullName 'bin\mysqld.exe'
        $mysqlProcess = Start-Process -FilePath $mysqlExecutable -ArgumentList ('--defaults-file="' + $mysqlConfiguration + '"') -WorkingDirectory $projectDirectory -WindowStyle Hidden -PassThru
        for ($attempt = 0; $attempt -lt 30 -and -not (Test-LocalPort -Port 3306); $attempt++) {
            if ($mysqlProcess.HasExited) {
                throw 'O MySQL não iniciou. Consulte .runtime/mysql-local/mysql.err.log.'
            }
            Start-Sleep -Milliseconds 500
        }
        if (-not (Test-LocalPort -Port 3306)) {
            throw 'O MySQL não respondeu na porta 3306.'
        }
    }

    if ($databaseTarget.local -or $AplicarMigracoes) {
        & $pythonExecutable -m app.database.migrate_music
        if ($LASTEXITCODE -ne 0) {
            throw 'Não foi possível aplicar as migrações. Confira as credenciais no .env.'
        }
    } else {
        Write-Host 'Banco remoto selecionado. Migrações e criação automática de tabelas estão desativadas.'
    }
    if (Test-LocalPort -Port 8000) {
        Write-Host 'Já existe uma aplicação na porta 8000. Encerre-a antes de iniciar outra instância.'
        return
    }
    & $pythonExecutable -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
} finally {
    Pop-Location
}
