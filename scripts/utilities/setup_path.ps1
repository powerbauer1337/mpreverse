# PowerShell script to add reverse engineering tools to PATH
$toolsDir = "C:\Users\marvi\Coding\MarsPro\assets\tools"

# Add apktool to PATH
$apktoolDir = Join-Path $toolsDir "apktool"
if (Test-Path $apktoolDir) {
    $env:PATH = "$apktoolDir;$env:PATH"
    Write-Host "Added apktool to PATH: $apktoolDir"
}

# Add jadx to PATH
$jadxDir = Join-Path $toolsDir "jadx\bin"
if (Test-Path $jadxDir) {
    $env:PATH = "$jadxDir;$env:PATH"
    Write-Host "Added jadx to PATH: $jadxDir"
}

Write-Host "Reverse engineering tools are now available in this session"
Write-Host "To make permanent, add these paths to your system PATH environment variable"
