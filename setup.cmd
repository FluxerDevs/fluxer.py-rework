@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "DISCORD_URL=https://github.com/Rapptz/discord.py.git"
set "DISCORD_BRANCH=v1.x"
set "DISCORD_DIR=discord.py"
set "FLUXER_URL=https://github.com/Fluxer-py/fluxer.py.git"
set "FLUXER_COMMIT=300d48e45deb88cbc1130b8749a5ad31cbc45d8b"
set "FLUXER_DIR=fluxer.py-old"
set "CHECK_ONLY=0"

if "%~1"=="--check" set "CHECK_ONLY=1"
if not "%~2"=="" goto :usage
if not "%~1"=="" if not "%~1"=="--check" goto :usage

where git >nul 2>nul
if errorlevel 1 (
    echo [setup] git is required but was not found on PATH.
    exit /b 1
)

if "%CHECK_ONLY%"=="1" (
    echo [setup] setup.cmd syntax check OK.
    exit /b 0
)

call :sync_discord || exit /b 1
call :sync_fluxer || exit /b 1

echo [setup] Done.
exit /b 0

:usage
echo Usage: setup.cmd [--check]
exit /b 2

:ensure_git_repo
set "TARGET=%~1"
if exist "%TARGET%" (
    if not exist "%TARGET%\.git" (
        echo [setup] Blocked: %TARGET% exists but is not an independent git checkout.
        exit /b 1
    )
)
exit /b 0

:ensure_clean
set "TARGET=%~1"
for /f "usebackq delims=" %%L in (`git -C "%TARGET%" status --porcelain`) do (
    echo [setup] Blocked: %TARGET% has uncommitted changes.
    exit /b 1
)
exit /b 0

:sync_discord
call :ensure_git_repo "%DISCORD_DIR%" || exit /b 1
if not exist "%DISCORD_DIR%" (
    echo [setup] Cloning %DISCORD_DIR% branch %DISCORD_BRANCH%...
    git clone --branch "%DISCORD_BRANCH%" --single-branch "%DISCORD_URL%" "%DISCORD_DIR%" || exit /b 1
    echo [setup] %DISCORD_DIR% cloned.
    exit /b 0
)
call :ensure_clean "%DISCORD_DIR%" || exit /b 1
echo [setup] Updating %DISCORD_DIR% to origin/%DISCORD_BRANCH%...
git -C "%DISCORD_DIR%" fetch origin "%DISCORD_BRANCH%" || exit /b 1
git -C "%DISCORD_DIR%" checkout "%DISCORD_BRANCH%" || exit /b 1
git -C "%DISCORD_DIR%" pull --ff-only origin "%DISCORD_BRANCH%" || exit /b 1
echo [setup] %DISCORD_DIR% is on %DISCORD_BRANCH%.
exit /b 0

:sync_fluxer
call :ensure_git_repo "%FLUXER_DIR%" || exit /b 1
if not exist "%FLUXER_DIR%" (
    echo [setup] Cloning %FLUXER_DIR%...
    git clone "%FLUXER_URL%" "%FLUXER_DIR%" || exit /b 1
    echo [setup] %FLUXER_DIR% cloned.
)
call :ensure_clean "%FLUXER_DIR%" || exit /b 1
echo [setup] Fetching %FLUXER_DIR% and checking out %FLUXER_COMMIT%...
git -C "%FLUXER_DIR%" fetch origin || exit /b 1
git -C "%FLUXER_DIR%" checkout --detach "%FLUXER_COMMIT%" || exit /b 1
echo [setup] %FLUXER_DIR% pinned to %FLUXER_COMMIT%.
exit /b 0

