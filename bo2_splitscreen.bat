
@echo off

echo warning: make sure Steam is running before proceeding

for /f "delims=" %%# in  ('"wmic path Win32_VideoController  get CurrentHorizontalResolution,CurrentVerticalResolution /format:value"') do (
  set "%%#">nul
)
set /a "VertHalf=%CurrentVerticalResolution%/2"
set /a "HorzHalf=%CurrentHorizontalResolution%/2"
 
echo %CurrentHorizontalResolution% x %CurrentVerticalResolution%

set /p id="Enter number of players (1-4): "
if %id%==1 (
	start Borderlands2.exe
	echo Launching game...
	exit
)

if %id%==2 (
	taskkill /f /im explorer.exe
	echo Insert controller for Player 1 and press any key on keyboard to continue. Wait to insert Player 2 controller 
	echo until Player 1 game menu is loaded.
	pause
	start Borderlands2.exe -WindowedFullscreen -AlwaysFocus -ResY=%VertHalf% -ResX=%CurrentHorizontalResolution% -SaveDataId=2 -WindowPosY=0
	echo Insert controller for Player 2 and press any key on keybaord to continue.
	pause
	start /min cmd /c "start /wait Borderlands2.exe -WindowPosY=%VertHalf% -AlwaysFocus -ResY=%VertHalf% -ResX=%CurrentHorizontalResolution% -ControllerOffset=1 -WindowedFullscreen & start explorer.exe" 

	
)

if %id%==3 (
	taskkill /f /im explorer.exe
	echo Insert controller for Player 1 and press any key on keyboard to continue. Wait to insert Player 2 controller until Player 1 game menu is loaded.
	pause
	start Borderlands2.exe -WindowedFullscreen -AlwaysFocus -ResY=%VertHalf% -ResX=%CurrentHorizontalResolution% -SaveDataId=2 -WindowPosY=0 -WindowPosX=0
	echo Insert controller for Player 2 and press any key on keybaord to continue. Wait to insert Player 3 controller until Player 2 game menu is loaded.
	pause
	start Borderlands2.exe -AlwaysFocus -ResY=%VertHalf% -ResX=%HorzHalf% -ControllerOffset=1 -WindowedFullscreen -WindowPosY=%VertHalf% -WindowPosX=0
	echo Insert controller for Player 3 and press any key on keybaord to continue.
	pause
	start /min cmd /c "start /wait Borderlands2.exe -AlwaysFocus -ResY=%VertHalf% -ResX=%HorzHalf% -ControllerOffset=2 -WindowedFullscreen -WindowPosY=%VertHalf% -WindowPosX=%HorzHalf% & start explorer.exe"
	
	
)	

if %id%==4 (
	taskkill /f /im explorer.exe
	echo Insert controller for Player 1 and press any key on keyboard to continue. Wait to insert Player 2 controller until Player 1 game menu is loaded.
	pause
	start Borderlands2.exe -WindowPosX=0 -WindowPosY=0 -WindowedFullscreen -AlwaysFocus -ResY=%VertHalf% -ResX=%HorzHalf% -SaveDataId=2 
	echo Insert controller for Player 2 and press any key on keybaord to continue. Wait to insert Player 3 controller until Player 2 game menu is loaded.
	pause
	start Borderlands2.exe -WindowPosX=%HorzHalf% WindowPosY=0 -AlwaysFocus -ResY=%VertHalf% -ResX=%HorzHalf% -ControllerOffset=1 -WindowedFullscreen 
	echo Insert controller for Player 3 and press any key on keybaord to continue. Wait to insert Player 4 controller until Player 3 game menu is loaded.
	pause
	start Borderlands2.exe -WindowPosY=%VertHalf% -WindowPosX=0 -AlwaysFocus -ResY=%VertHalf% -ResX=%HorzHalf% -ControllerOffset=2 -WindowedFullscreen 
	echo Insert controller for Player 4 and press any key on keybaord to continue.
	pause
	start /min cmd /c "start /wait Borderlands2.exe -WindowPosY=%VertHalf% -WindowPosX=%HorzHalf% -AlwaysFocus -ResY=%VertHalf% -ResX=%HorzHalf% -ControllerOffset=2 -WindowedFullscreen & start explorer.exe"

	
)

