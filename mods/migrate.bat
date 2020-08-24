:: PATH to World of Warships game.
IF NOT "%1" == "" ( SET region=%1) ELSE ( SET region=NA)
SET installed_drive=

:: #1. Find the drive in which WOWs is installed.
for %%x in (C, D, E, F) do (
    IF EXIST "%%x:\Games\World_of_Warships_%region%" (
        SET installed_drive=%%x
    )
)

IF "%installed_drive%" == "" (
    echo GAME_NOT_FOUND
    GOTO:EOF
) ELSE ( echo "GAME: %installed_drive%" )

SET game_path=%installed_drive%:\Games\World_of_Warships_%region%\bin
FOR /D %%d in ("%game_path%\*") DO (
    SET build_path=%%d
)

FOR /D %%d in ("%build_path%\res_mods\*") DO (
    SET version_path=%%d
)

IF NOT EXIST %version_path%\PnFMods ( mkdir %version_path%\PnFMods )

$null > %version_path%\PnFModsLoader.py

IF NOT EXIST %version_path%\PnFMods\AutoMod ( mkdir %version_path%\PnFMods\AutoMod )

copy Main.py %version_path%\PnFMods\AutoMod\Main.py