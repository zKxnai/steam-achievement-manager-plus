# Steam Achievement Manager Plus (SAM+)
- New version of SAM
- Rewritten in Python
- Source Code in C#: https://github.com/gibbed/SteamAchievementManager
- Current State: Beta 0.6.7

## (New) Key features
- View and edit Steam achievement for every owned game
- Gain playtime without starting the game
- Updated UI and look
- News feed
- Tabs (Achievements, News, Observed Games)
- Show achievement count

## ToDo
### Unfinished

- Observe game achievements (For games that gradually add more achievements)
    - ~~Button left of Favorite button~~
    - ~~Adds game to Observed games tab~~
    - Load icons
    - Saves observed games
    - Shows count of earned achievements, missing achievements and percentage of completion
    - Placeholder (Loading achievements...) for background loading, update when fetched
    - Progressbar for achievement completion
- Optimize performance (Eliminate glitches while scrolling, etc.)
    - Increase FPS
    - Limit resource usage
- Only show game which count against game completion rate
- Get every game listed (Mods counted as Games etc.)
- Open achievements in custom window
- Different themes/switches (Toggle on/off automatically)

### Finished
- ~~Load icons in background~~
- ~~Search for/Jump to game via name/AppID~~
- ~~Tide up code~~
- ~~Make list scrollable~~
- ~~Small adjustments: qop4, shapez should appear ad Q and S~~
- ~~Change grid view to list view? + Change Images to Icons~~
- ~~Play and pause button to just farm playtime~~
- ~~Resize grid by window size~~
- ~~Add info at top right, how many games are displayed~~
- ~~Add button functionality~~
- ~~Show when game is played~~
- ~~Show how many games are played~~
- ~~Add Tab function:~~
- ~~API Key fix~~
- ~~Add "Lightmode" tab~~(Impossible due to selected theme)
    - ~~Change to Lightmode~~
    - ~~Change background color~~
    - ~~Change other things (font, etc.)~~
    - ~~Tab placement rightside~~
**~~!!!Create Landing Page!!!~~**
- ~~Fix implementation of achievements tab~~
    - ~~Fix Icon loading~~
    - ~~Fix "Playing..." in green~~
- ~~Favorite games~~ (Can be done with observing)
    - ~~Heart/Star button right of achievement button~~
    - ~~Shown at the top of games list~~
- ~~Separate code for better overview~~
- ~~Fix scrolling in achievements tab after implementation in news tab~~
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
- ~~Scrolling only works in active tab~~