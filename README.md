# Steam Achievement Manager Plus (SAM+)
- New version of SAM
- Rewritten in Python
- Source Code in C#: https://github.com/gibbed/SteamAchievementManager
- Current State: Beta 0.8.3

## (New) Key features
- View and edit Steam achievement for every owned game
- Gain playtime without starting the game
- Updated UI and look
- News feed
- Tabs (Achievements, News, Observed Games)
- Show achievement count

## ToDo
<details>
<summary>Unfinished</summary>

#### General
- Optimize performance
    - Increase FPS
    - Limit resource usage
    - Profiling implementation(?)
    - Eliminate glitches while scrolling
- Info bar instead of Popups

#### Landing Page:

#### Achievements:
    - Pin Icon to pin specific games at the top
    - Progressbar
    - Achievementcount
    - Save pinned games in database

#### News:

#### Observed Games: (Integrated into Achievements)

#### Appearance:
- Optional: Implement ScrollableFrame (When more themes get added)

</details>
<details>
<summary>Finished</summary>

#### General
- ~~Tide up code~~
- ~~Add Tab function:~~
- ~~API Key fix~~
- ~~Separate code for better overview~~
- ~~Scrolling only works in active tab~~
- ~~README with collapsible headers(?)~~
- ~~Save additional files/content internally~~
- ~~Icons next to tabs~~
- ~~Tide up Resources~~
- ~~Steam-API-Key fix~~
    - ~~Dedicated tab~~
    - ~~Instructions how to gain Web-API key~~
    - ~~Get key from database~~

#### Landing Page:
**~~!!!Create Landing Page!!!~~**

#### Achievements:
- ~~Load icons in background~~
- ~~Search for/Jump to game via name/AppID~~
- ~~Make list scrollable~~
- ~~Small adjustments: qop4, shapez should appear ad Q and S~~
- ~~Change grid view to list view? + Change Images to Icons~~
- ~~Play and pause button to just farm playtime~~
- ~~Resize grid by window size~~
- ~~Add info at top right, how many games are displayed~~
- ~~Add button functionality~~
- ~~Show when game is played~~
- ~~Show how many games are played~~
- ~~Fix implementation of achievements tab~~
    - ~~Fix Icon loading~~
    - ~~Fix "Playing..." in green~~
- ~~Fix scrolling in achievements tab after implementation in news tab~~
- ~~Get every game listed (Mods counted as Games etc.)~~
- ~~Open achievements in custom window~~
    - ~~Focus window when opening~~
    - ~~Edit SAM.Game.exe~~
    - ~~SAM+ Darkmode -> SAM.Game.exe Darkmode/ SAM+ Lightmode -> SAM.Game.exe Lightmode~~
    - ~~Fix first Startup "Cant find window error" -> Change Title Bar SAM.Game.exe~~
    - ~~Fix Buttons Functions Achievement Window -> Change Title Bar SAM.Game.exe~~

#### News:
- ~~FIX news entry cleaning~~
- ~~News feed~~
    - ~~Optimize searchbar (Jump to and text inside disappears when typing)~~
    - ~~Add searchbar~~
    - ~~Better UI (fix HTML tags)~~
    - ~~FIX NEWS NOT SHOWING UP~~
    - ~~Make scrollable with mouse scroll~~
    - ~~Fix unlimited loading of zup s!~~
    - ~~Fix Refresh button~~
    - ~~Show date/convert timestamp~~
    - ~~Place Refresh button top right corner~~
    - ~~Load asynchronously~~

#### Observed Games: (Integrated into Achievements)
- ~~Favorite games~~ (Can be done with observing)
    - ~~Heart/Star button right of achievement button~~
    - ~~Shown at the top of games list~~
- ~~Observe game achievements (For games that gradually add more achievements)~~
    - ~~Button right of Achievements button~~
    - ~~Adds game to Observed games tab~~
    - ~~Load icons~~
    - ~~Shows count of earned achievements, missing achievements and percentage of completion~~
    - ~~Placeholder (Loading achievements...) for background loading, update when fetched~~
    - ~~Progressbar for achievement completion~~
    - ~~Save observed games in database~~

#### Appearance:
- ~~Add "Lightmode" tab~~
-   ~~Change to Lightmode~~
-   ~~Change background color~~
-   ~~Change other things (font, etc.)~~
-   ~~Tab placement rightside~~
- ~~Implement customtkinter~~
- ~~FIX Forest Theme Integration~~
- ~~Different themes/switches (Toggle on/off automatically)~~
- ~~Default theme label~~
- ~~Current theme label~~
- ~~Default theme button~~
- ~~Updating default theme label~~
- ~~Updating current theme label~~
- ~~Fix Sun Valley Dark/Light in Default theme~~
- ~~Pop-Up window for confirmation of theme change~~
</details>