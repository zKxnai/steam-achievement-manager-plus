# Steam Achievement Manager Plus (SAM+)
- New version of SAM
- Rewritten in Python
- Source Code in C#: https://github.com/gibbed/SteamAchievementManager
- Current State: Beta 0.6.7.4

## (New) Key features
- View and edit Steam achievement for every owned game
- Gain playtime without starting the game
- Updated UI and look
- News feed
- Tabs (Achievements, News, Observed Games)
- Show achievement count

## ToDo
### Unfinished
- Optimize performance (Eliminate glitches while scrolling, etc.)
    - Increase FPS
    - Limit resource usage
    - Profiling implementation(?)
- README with collapsible headers(?)

#### Landing Page:

#### Achievements:
- Only show game which count against game completion rate
- Get every game listed (Mods counted as Games etc.)
- Open achievements in custom window

#### News:

#### Observed Games:
- Observe game achievements (For games that gradually add more achievements)
    - Button left of Favorite button
    - Adds game to Observed games tab
    - Load icons
    - Saves observed games
    - Shows count of earned achievements, missing achievements and percentage of completion
    - Placeholder (Loading achievements...) for background loading, update when fetched
    - Progressbar for achievement completion

#### Appearance:
- Default theme button

### Finished
- ~~Tide up code~~
- ~~Add Tab function:~~
- ~~API Key fix~~
- ~~Separate code for better overview~~
- ~~Scrolling only works in active tab~~

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

#### Observed Games:
- ~~Favorite games~~ (Can be done with observing)
    - ~~Heart/Star button right of achievement button~~
    - ~~Shown at the top of games list~~

#### Appearance:
- ~~Add "Lightmode" tab~~
-   ~~Change to Lightmode~~
-   ~~Change background color~~
-   ~~Change other things (font, etc.)~~
-   ~~Tab placement rightside~~
- ~~Implement customtkinter~~
- ~~FIX Forest Theme Integration~~
- ~~Different themes/switches (Toggle on/off automatically)~~