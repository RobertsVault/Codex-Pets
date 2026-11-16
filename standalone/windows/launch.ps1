param([ValidateSet('mikan','doubao','enable-hooks','disable-hooks')][string]$Mode = 'doubao', [ValidateSet('auto','zh','en')][string]$Language = 'auto')
$ErrorActionPreference = 'Stop'
$python = $null
$prefix = @()
$candidates = @()
$launcher = Get-Command py.exe -ErrorAction SilentlyContinue
if ($launcher) { $candidates += @{ Path = $launcher.Source; Prefix = @('-3') } }
$candidate = Get-Command python.exe -ErrorAction SilentlyContinue
if ($candidate -and $candidate.Source -notmatch '\\Microsoft\\WindowsApps\\') {
    $candidates += @{ Path = $candidate.Source; Prefix = @() }
}
foreach ($item in $candidates) {
    $testPrefix = $item.Prefix
    try {
        & $item.Path @testPrefix -c 'import sys, tkinter; assert sys.version_info >= (3,10)' 2>$null
        if ($LASTEXITCODE -eq 0) { $python = $item.Path; $prefix = $item.Prefix; break }
    } catch { continue }
}
if (!$python) { throw 'Install Python 3.10+ with Tcl/Tk, then try again.' }
if ($Mode -notin @('enable-hooks','disable-hooks')) {
    $pillowReady = $false
    try {
        & $python @prefix -c 'from PIL import Image, ImageDraw, ImageFont' 2>$null
        $pillowReady = ($LASTEXITCODE -eq 0)
    } catch { $pillowReady = $false }
    if (!$pillowReady) {
        & $python @prefix -m pip install --user -r (Join-Path $PSScriptRoot 'requirements.txt')
        if ($LASTEXITCODE -ne 0) { throw 'Pillow installation failed. Install requirements.txt and retry.' }
    }
}
if ($Mode -in @('enable-hooks','disable-hooks')) {
    $options = @()
    if ($Mode -eq 'disable-hooks') { $options = @('--remove') }
    & $python @prefix (Join-Path $PSScriptRoot 'desktop/setup_hooks.py') @options
    if ($LASTEXITCODE -ne 0) { throw 'Hook configuration failed.' }
} else {
    $script = Join-Path $PSScriptRoot 'desktop/companion.py'
    $quotedScript = '"' + $script + '"'
    $arguments = @($prefix) + @($quotedScript,'--pet',$Mode)
    if ($Language -ne 'auto') { $arguments += @('--language',$Language) }
    $data = $env:CODEX_PETS_DATA
    if (!$data) { $data = Join-Path $env:LOCALAPPDATA 'CodexPets' }
    New-Item -ItemType Directory -Path $data -Force | Out-Null
    $instance = [guid]::NewGuid().ToString('N')
    $process = Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardError (Join-Path $data "$Mode-$instance.error.log") -RedirectStandardOutput (Join-Path $data "$Mode-$instance.output.log") -PassThru
    Write-Output "Started $Mode (PID $($process.Id))"
}
