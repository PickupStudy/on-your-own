@echo off
setlocal EnableExtensions

cd /d "%~dp0.." || exit /b 1

if not exist ".env" (
  echo Missing .env. Copy .env.example to .env first.
  exit /b 1
)

for %%I in (".env") do if %%~zI==0 (
  echo .env is 0 bytes — save your editor ^(Ctrl+S^) then retry.
  exit /b 1
)

node ".\node\src\main.js" pipeline
exit /b %ERRORLEVEL%
