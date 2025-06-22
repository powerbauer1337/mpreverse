@echo off
setlocal enabledelayedexpansion

echo Setting up GitHub repository for MarsPro project...
echo.

REM Check if git is available
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git not found. Please install Git first:
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Git found
echo.

REM Get repository URL from user
set /p REPO_URL="Enter your GitHub repository URL (e.g., https://github.com/username/marspro-analysis.git): "

if "%REPO_URL%"=="" (
    echo Repository URL is required
    pause
    exit /b 1
)

echo.
echo Initializing git repository...
git init

echo Adding files to repository...
git add .

echo Creating initial commit...
git commit -m "Initial commit: MarsPro reverse engineering and Home Assistant integration"

echo Adding remote repository...
git remote add origin %REPO_URL%

echo Setting branch name to 'main'...
git branch -M main

echo Pushing to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo Repository setup complete!
    echo Your repository is now available at: %REPO_URL%
) else (
    echo Failed to push to GitHub. Please check your repository URL and permissions.
)

echo.
pause 