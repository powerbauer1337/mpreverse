@echo off
REM Batch script to add reverse engineering tools to PATH
set TOOLS_DIR=C:\Users\marvi\Coding\MarsPro\assets\tools

REM Add apktool to PATH
set APKTOOL_DIR=%TOOLS_DIR%\apktool
if exist "%APKTOOL_DIR%" (
    set PATH=%APKTOOL_DIR%;%PATH%
    echo Added apktool to PATH: %APKTOOL_DIR%
)

REM Add jadx to PATH
set JADX_DIR=%TOOLS_DIR%\jadx\bin
if exist "%JADX_DIR%" (
    set PATH=%JADX_DIR%;%PATH%
    echo Added jadx to PATH: %JADX_DIR%
)

echo Reverse engineering tools are now available in this session
echo To make permanent, add these paths to your system PATH environment variable
