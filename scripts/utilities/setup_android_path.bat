@echo off
REM Batch script to add Android tools to PATH
set TOOLS_DIR=C:\Users\marvi\Coding\MarsPro\assets\tools

REM Add Android Platform Tools to PATH
set ANDROID_TOOLS_DIR=%TOOLS_DIR%\android-platform-tools
if exist "%ANDROID_TOOLS_DIR%" (
    set PATH=%ANDROID_TOOLS_DIR%;%PATH%
    echo Added Android Platform Tools to PATH: %ANDROID_TOOLS_DIR%
)

echo Android development tools are now available in this session
echo To make permanent, add these paths to your system PATH environment variable
