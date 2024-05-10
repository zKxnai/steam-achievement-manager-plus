# Steam Achievement Manager Plus (SAM+)
- New version of SAM
- Rewritten in Python
- Source Code in C#: https://github.com/gibbed/SteamAchievementManager
- Current State: Beta 0.6.4

## (New) Key features
- View and edit Steam achievement for every owned game
- Gain playtime without starting the game
- Updated UI and look
- News feed
- Tabs (Achievements, News, Observed Games)
- Show achievement count

## ToDo
### Unfinished

**~~!!!Create Landing Page!!!~~**
- ~~Fix implementation of achievements tab~~
    - ~~Fix Icon loading~~
    - ~~Fix "Playing..." in green~~

- Observe game achievements (For games that gradually add more achievements)
    - ~~Button left of Favorite button~~
    - ~~Adds game to Observed games tab~~
    - Load icons
    - Saves observed games
    - Shows count of earned achievements, missing achievements and percentage of completion
    - Placeholder (Loading achievements...) for background loading, update when fetched
    - Progressbar for achievement completion
- Optimize performance (Eliminate glitches while scrolling, etc.) (In separate file)
    - Increase FPS
    - Limit resource usage
- Favorite games
    - Heart/Star button right of achievement button
    - Shown at the top of games list
- Only show game which count against game completion rate
- Get every game listed (Mods counted as Games etc.)
- Open achievements in custom window
- Separate code for better overview
- Prevent Cursor from automatically tapping in searchbar
- Scrolling only works in active tab
- ~~Search for/Jump to game via name/AppID~~ with highlight
- News feed
    - Make scrollable with mouse scroll
    - Better UI (fix HTML tags)
    - Fix unlimited loading of zup s!
    - Optimize searchbar (Jump to and text inside disappears when typing)
    - ~~Add searchbar and lightmode toggle~~
    - ~~Fix Refresh button~~
    - Show date/convert timestamp
    - ~~Place Refresh button top right corner~~
    - Load asynchronously

### Finished
- ~~Load icons in background~~
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