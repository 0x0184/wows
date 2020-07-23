:: PATH to World of Warships game.
set path="C:\Games\World_of_Warships_ASIA\bin\2697511\res_mods\0.9.6.1"

if not exist %path%\PnFMods ( mkdir %path%\PnFMods )

$null > %path%\PnFModsLoader.py

echo %path%

if not exist %path%\PnFMods\AutoMod ( mkdir %path%\PnFMods\AutoMod )

copy Main.py %path%\PnFMods\AutoMod\Main.py