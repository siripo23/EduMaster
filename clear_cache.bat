@echo off
echo ========================================
echo Browser Cache Cleaner
echo ========================================
echo.
echo This will help clear browser cache
echo.
echo INSTRUCTIONS:
echo 1. Close ALL browser windows first
echo 2. Press any key to continue
echo 3. Follow the instructions
echo.
pause

echo.
echo Clearing Chrome cache...
if exist "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache" (
    rd /s /q "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache"
    echo Chrome cache cleared!
) else (
    echo Chrome cache not found
)

echo.
echo Clearing Edge cache...
if exist "%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache" (
    rd /s /q "%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache"
    echo Edge cache cleared!
) else (
    echo Edge cache not found
)

echo.
echo Clearing Firefox cache...
if exist "%LOCALAPPDATA%\Mozilla\Firefox\Profiles" (
    for /d %%i in ("%LOCALAPPDATA%\Mozilla\Firefox\Profiles\*") do (
        if exist "%%i\cache2" (
            rd /s /q "%%i\cache2"
            echo Firefox cache cleared!
        )
    )
) else (
    echo Firefox cache not found
)

echo.
echo ========================================
echo Cache clearing complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start your Flask app: python run.py
echo 2. Open browser
echo 3. Go to: http://127.0.0.1:5000/color-test
echo 4. Check if colors are correct
echo.
pause
