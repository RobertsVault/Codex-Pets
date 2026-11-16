param([string]$Destination = $(if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'pets' } else { Join-Path $HOME '.codex/pets' }))
$ErrorActionPreference = 'Stop'
$Destination = [System.IO.Path]::GetFullPath($Destination)
$backupRoot = Join-Path (Split-Path $Destination -Parent) 'pet-backups'
foreach ($name in @('mikan', 'doubao')) {
    $source = Join-Path $PSScriptRoot "pets/$name"
    $manifest = Get-Content -LiteralPath (Join-Path $source 'pet.json') -Raw | ConvertFrom-Json
    if ($manifest.spriteVersionNumber -ne 2 -or !(Test-Path -LiteralPath (Join-Path $source $manifest.spritesheetPath))) {
        throw "Invalid pet package: $name"
    }
}
New-Item -ItemType Directory -Path $Destination -Force | Out-Null
New-Item -ItemType Directory -Path $backupRoot -Force | Out-Null
foreach ($name in @('mikan', 'doubao')) {
    $target = Join-Path $Destination $name
    $backup = Join-Path $backupRoot "$name-$([guid]::NewGuid().ToString('N'))"
    $staging = "$target.install-$([guid]::NewGuid().ToString('N'))"
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot "pets/$name") -Destination $staging -Recurse
    try {
        if (Test-Path -LiteralPath $target) { Move-Item -LiteralPath $target -Destination $backup }
        Move-Item -LiteralPath $staging -Destination $target
    } catch {
        if (!(Test-Path -LiteralPath $target) -and (Test-Path -LiteralPath $backup)) { Move-Item -LiteralPath $backup -Destination $target }
        throw
    }
    Write-Host "Installed $name. Previous version, if present: $backup"
}
Write-Host 'Done. Refresh the custom pets list in Codex, or restart Codex.'
