@echo off
REM Xialiao Monitor - Push to GitHub
echo ========================================
echo Xialiao Monitor - Publishing to GitHub
echo ========================================
echo.

cd /d "%~dp0"

REM Check if git is initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
)

REM Add all files
echo Adding files...
git add -A

REM Commit
echo Committing changes...
git commit -m "feat: 虾聊社区监控技能 v1.0.0"

REM Set branch name
git branch -M main

REM Add remote (if not exists)
git remote remove origin 2>nul
git remote add origin https://github.com/hotice888/xialiao-monitor.git

REM Push to GitHub
echo.
echo ========================================
echo Pushing to GitHub...
echo ========================================
echo Please enter your GitHub credentials when prompted.
echo.
git push -u origin main --force

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Published to GitHub
    echo ========================================
    echo Repository: https://github.com/hotice888/xialiao-monitor
    echo.
) else (
    echo.
    echo ========================================
    echo FAILED! Please check your GitHub credentials
    echo ========================================
    echo.
)

pause
