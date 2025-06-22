# PowerShell script to add Android tools to PATH
$toolsDir = "C:\Users\marvi\Coding\MarsPro\assets\tools"

# Add Android Platform Tools to PATH
$androidToolsDir = Join-Path $toolsDir "android-platform-tools"
if (Test-Path $androidToolsDir) {
    $env:PATH = "$androidToolsDir;$env:PATH"
    Write-Host "Added Android Platform Tools to PATH: $androidToolsDir"
}

Write-Host "Android development tools are now available in this session"
Write-Host "To make permanent, add these paths to your system PATH environment variable"
