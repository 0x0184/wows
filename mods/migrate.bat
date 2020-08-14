:: PATH to World of Warships game.
IF NOT "%1" == "" ( SET region=%1) ELSE ( SET region=NA)
SET installed_drive=

:: #1. Find the drive in which WOWs is installed.
for %%x in (C, D, E, F) do (
    IF EXIST "%%x:\Games\World_of_Warships_%region%" (
        echo "Answer: %%x"
        SET installed_drive=%%x
    )
)

IF "%installed_drive%" == "" (
    echo GAME_NOT_FOUND
    exit
) ELSE (
    echo "GAME: %installed_drive%"
)

SET path="%installed_drive%:\Games\World_of_Warships_%region%\bin\2744482\res_mods\0.9.7.0"

IF NOT EXIST %path%\PnFMods ( mkdir %path%\PnFMods )

$null > %path%\PnFModsLoader.py

echo %path%

IF NOT EXIST %path%\PnFMods\AutoMod ( mkdir %path%\PnFMods\AutoMod )

copy Main.py %path%\PnFMods\AutoMod\Main.py