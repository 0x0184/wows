:: PATH to World of Warships game.
IF NOT "%1" == "" ( SET region=%1) ELSE ( SET region=NA)

SET path="C:\Games\World_of_Warships_%region%\bin\2744482\res_mods\0.9.7.0"

IF NOT EXIST %path%\PnFMods ( mkdir %path%\PnFMods )

$null > %path%\PnFModsLoader.py

echo %path%

IF NOT EXIST %path%\PnFMods\AutoMod ( mkdir %path%\PnFMods\AutoMod )

copy Main.py %path%\PnFMods\AutoMod\Main.py