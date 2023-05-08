@echo off
cd /d public_test_data

for %%i in (*.lsp) do (
    echo %%i:
    python ../Main.py -f %%i
    echo.
)
