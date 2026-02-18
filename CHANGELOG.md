# Version changelog

### 1.2

- New main menu option: "_Add blob name suggestion_"
  - Here the user can add a name to the name suggestions list
  - When a new blob is created and the name suggestions list is not empty, it takes the oldest record of the list and applies the name to the blob thus the simulation is not blobked
  - If the name suggestions list is empty the blob creation is the same as in previous versions
- Enhanced prompt for entering blob name: a dialog window appears with a textbox

### 1.2.1

- App crash at the end of the last league event of season fixed

### 1.2.2

- Fixed the contract problem in inactive leagues at the end of season
- Fixed calendar creation at the end of season
- Debug mode window title extended with "_debug mode_"
- Started removing types of the typing library from the code as newer python versions provide native list and dict types

### 1.2.3

- Changed disclaimer text on intro screen
- Visual representation of a blob is created in vector image format

### 1.2.4

- Fixed standings sorting on score ties

### 1.2.5

- Created unit test environment, writing tests for league service

### 1.2.6

- Fixed bug: empty grandmasters standings table appears for next eon when season is dividable by 4
- On the league standings for current season blob names are colored when their contract is ending this season
- Grandmaster winners get 1 extra season for their contract
- Wrote tests for championship service

### 1.2.7

- For larger field sizes the elimination count calculation changed to align with the rules
- Improving the progress simulation view by adding a GUI window to show the progress of the process

### 1.3

- Added new race event format: endurance race event

### 2.0

- Migrates UI to a web based frontend application
  - The UI consists of a main area where the contents of the different pages are rendered and menu bar on the left to navigate between these pages
  - the pages follow a similar structure to the previous Console UI
  - The pages are the following:
    - Dashboard
    - Blobs
    - Standings
    - Calendar
    - Event pages
- Adjusted application setup and startup logic
  - A `setup` script is added which installs the backend and frontend dependencies
  - The `start` and `debug` scripts start the backend and frontend as well in production and development mode respectively
  - Added possibility to run the app on Linux distributions
- New page: Factory
  - Shows factory progress on a progress bar
  - Lists blob name suggestions and a button
  - Clicking the button a dialog appears where the user can add a new name suggestion
  - The same name validations apply as on the old UI
- Added new simulation status texts, now called as "news":
  - When a blob is created and named after a suggested name, that name is displayed
  - After an event is concluded a sumamry text is shown with the top 3

### 2.1

- Blobs now can have children, by becoming grandmaster at the end of each eon
- Children inherit the last name of the grandmaster
- On blob creation children get bonuses to initial stats:
  - +0.01 learning for every championship title of parent
  - +0.01 strength for every grandmaster title of parent
  - So if parent is currently 5 times champion and 2 times grandmaster, then their new child gets 0.05 learning and 0.02 strength bonus

### 2.1.1

- Fixed missing adjustments related to the name split

### 2.1.2

- Fixed error on event record calculation if field size is 15 or larger
- Cached event records table on quartered event page so it does not disappears for a moment, causing unintended scrollup

### 2.2

- Each blob has a unique color
- Added blob icons to the blob list
  - The icon is displayed next to the blob's name
- Added blob details dialog when clicking on a blob in the blobs page
  - Shows blob in large
  - Displays blob's basic information like birthdate, debut, current status
  - Shows blob's achievements like podiums, wins, championships and grandmaster titles
- Added copyright text and version to the bottom of the menubar

### 2.2.1

- Improved UI responsiveness so the UI is more usable on mobile
- Landscape mode on mobile is still a bit broken, will be refined in future release

### 2.3

- Added admin authentication
  - Login page with username and password
  - Token-based authentication with backend API
  - Protected endpoints that require authentication
  - Only admin user is added at the moment, no registration

### 2.3.1

- Smaller UI fixes on blobs page and race event page

### 2.3.2

- On race events score generation use perlin-like noise for more diverse race results
- Fixed competitor shuffling at the beginning of events
- Added event records cache to endurance race view to avoid table flashing on progressing to next tick

### 2.3.3

- Hide "add name suggestion" button and progress buttons on event page when user is unauthorized
- Minor refactors on dashboard

### 2.3.4

- Display name of blob's parent on blob details dialog

### 2.4

- Introduce internationalization:
  - Language can be set at the bottom of the drawer
  - Default language is english
  - Other language option is hungarian
- Fixed blob search by name error
- Adjusted blob datagrid autosizing to solve column grid imploding

### 2.5

- Adjusted application to be hosted on the internet
- Migrated database to Postgres
- Adjusted database migrations for postgres and populate initial data as current state of the "production" database
- Adjusted frontend to enable setting backend url from environment variables

### 2.5.1

- Some hotfixes to production deployment
- When user is logged in redirect from login to dashboard
- Proceed to event button is green and visible for non logged in users too
- At the first quarter in high jump events the randomized starting is fixed with a twist: the order of blobs that not scored yet is randomized every tick
- Improved backend error logging

### 2.5.2 - Miscellaneous update

- Reworked the calendar on desktop view to make the calendar more visual
  - No room for the new design in mobile view, it will be reworked later
- Fixed action multiplicating bug in endurance races
  - Disable simulation and event progression buttons when progression related operations are pending
  - Backend throws error when actions are about to be saved for a tick, but there are already saved actions corresponding for that tick
- Fixed page sizing problems on standings page mobile
- Fixed page sizing problems on endurance event page mobile

### 2.5.3

- On race events if a blob overtakes someone or is overtaken, they learn from it, so their strength increases a little bit
- Added playback flag for race events to avoid duplicated rewards for overtakes on page reloads
- When a blob sets a new record on a quartered high jump event, a snackbar appears to notify the user about the new record

### 2.6 - Stats update

- Blobs get a new stat: speed
  - Used for score generation in race events
  - During practice, the practice effect is divided between the two stats in random ratio
- Modified stat update multiplyer constants
- Added backend checks for simulation progress endpoint
- Generalised loading animation
- Refined desktop calendar to display only the current season's epochs and all of the events in the current season

### 2.6.1 Hotfix

- Updated openapi specifications to fix the quartered event action creation error
- Fixed login page layout issues

### 2.6.2

- Fixed bug about getting error when saving quartered event results
- Added error snackbar when result save and event record assembly runs into an error

### 2.6.3

- Fixed to show mobile drawer menu when mobile device is in landscape mode

### 3.0

- Added rookie of the year feature: if there are at least three rookies participated in a league at the end of the season the best rookie gets money reward and a contract extension
- Reworked actions data structure:
  - Instead of storing every score one by one they are now grouped by event and competitor
  - Event ticks and which score belongs to which tick is calculated from event rules
  - DISCLAIMER (for dev): because of the previous point, event rules should be versioned, if they are changed in the future
- Seed for score generation in race events are calculated from blob id instead of speed because speed can change during event
- Enhanced event progresion handling:
  - Every click on the ProgressButton can be done by pressing _space_
  - Enchanced quartered event UI to display current blob with shadow box instead of darker border
- Blobs with ending contract and rookies are now marked with badges instead of colored background
- Score generation for quartered events now require both skill stats from blobs: strength 70%, speed 30%
  - Skills are updated after event accordingly
- New event type: elimination scoring
  - Scores generated from blob strength
  - In each tick every non eliminated blob generates a score and the lowest scoring gets eliminated
  - This repeats until only one blob is left
- Fixed bug: event result saving was possibble multiple times after event was concluded
- Added new information to blob details dialog to display:
  - Strength, speed and integrity state relative to other blobs (no exact values, just categories with color code)
  - Termination and retirement dates
  - Money
  - If blob is dead, a different blob icon is displayed
  - Current activity
- Added minor blinking animation to blob on blob details dialog
- Reworked blob activity logic to first proceed with the effects of the current activity stored in the database then generate the activities for next cycle (day)
- Blob details dialog now can be opened on standings and event pages by clicking on blob name
- Reworked news logic:
  - News entries are saved to database
  - Whole new variety of news:
    - Blob created, terminated, retired, debuted
    - Event starteing, ongoing, ened (displaying results)
    - Season ended for league, displaying champion
    - New season started, displaying league transfers, retirees and debuting blobs
    - New grandmaster at the start of new eon
- Refactored UI:
  - Added app header bar with page title and menu toggle button in mobile mode
  - Page title card is removed
  - News card redesigned according to the reworked news logic
  - Control buttons like 'Next day', 'Proceed to event' are put to a toolbar card at the bottom

### 3.0.1

- Fixed production build error caused by vite version update

### 3.0.2

- Fixed best score calculation error in quartered events
- Fixed news text translation issues

### 3.0.3

- Added speed stat bonus for grandmaster's child

### 3.1

- Added cathup trainings:
  - On the second epoch of every season
  - The following blobs participate:
    - The youngest blob to debut
    - Last seasons last place of every league
    - Every blob demoted to the dropout league last season
- Added intense training
  - Done only on cathup trainings
  - More efficient than regular practice
- Added blob icons next to names in news
- By clicking on the blob icon and name in the news the blob details dialog opens
- Fixed new season news querying

### 3.1.1

- Fixed news text for "rookie of the year" and "season ended" news types
- Fixed bug about blob order is not randomized when event starts

### 3.1.2

- Created records database table to make record checking and managing logic simpler and mor robust
- Created endpoints for querying records for possible future feature
- Fixed bug about blob dialog not opening from news of certain types
- Fixed issue about the "NEW_GRANDMASTER" news type appearing at the end of every season

### 3.1.3

- Extended bonus point calculation to elimination event:
  - If a blob scores highest in at least one tick they get one bonus point
  - The blob with the most ticks won gets an additional bonus point (if there is a tie then no bonus points given)
  - The winner of the whole event gets one additional bonus point
- Adjusted UI on elimination event so the latest eliminated blob's score is displayed
- Fixed elimination event table aligning against the barchart
- Added missing rounding to elimination score record
- Fixed starting event news round calculation bug

### 3.1.4

- Fixed missing browser shortcut icon
- Fixed page overflow issue on mobile caused by browser header on scrolling

### 3.1.5

- Fixed scrolling issue on event and factory page

### 3.2

- Changed skill effect of overtakes in endurance races: the blob overtaken now improves their speed skill with the same modifier as the one overtook them
- Enhanced blob visualization:
  - Blobs on blob details dialog has an idle animation of "extending" and "retracting" vertically
  - The current grandmaster has a crown on their head
- Fixed error on opening the blob details dialog for a terminated blob

### 3.3

- Made news loading independent from the other loading processes on dashboard
  - Added skeleton loader to news card
- Removed strength and speed indicator from blob details dialog
- Replaced top 3 blobs in event ended news with a link
  - Opens a modal containing the event results

### 3.4 - Grandmaster activity update

- Added grandmaster "Administration" activity allowing grandmasters to randomly create temporary "policies" (Factory modernization, Gym improvements, Salary raise, Pension).
  - Policies have duration depending on grandmaster level (level 1 → 4 days; level 2 → 6 days; level >2 → 6 + (level - 2) days) and an applied level determining effect strength.
  - Effects: factory modernization speeds up factory progress; gym improvements increase practice/intense training efficiency; salary raises increase labour salary; pension schemes provide pension payouts to retired blobs.
  - Backend: new `policies` DB table, repository upsert, domain service to create/update policies, and an API endpoint (`GET /policies/`) returning active policies. Added Alembic migrations (policies table + ADMINISTRATION activity enum value) and unit tests.
  - Frontend: Dashboard "Policies" panel showing active policies with tooltips and translations added (English & Hungarian).

- Bugfix: Fixed Results modal so it properly refreshes/resets on open/close to avoid stale state and duplicated fetches.
- Bugfix: Results table on the modal displays name shorthands on mobile devices

### 3.5 - Sprint and Mining update

- added new event type: sprint race
  - blobs have a certain amount of time to finish the race of a given distance
  - the available time is determined the same way as for endurance races
  - the distance to make during the race is the same amount of distance units as the number of available ticks
  - point system is the same as for endurance races with one addition:
    - contenders who cannot finish the given time in the available time get one point less as the base points determined by finishing position
  - from the four guaranteed event types Quartered two shot high jump is replaced by sprint race
- added new activity: mining
  - from the blobs who chose to mine in the current cycle one is chosen as winner
  - the winner gets the same amount of coins as the number of blobs participated in mining
- added visualization for the following activities:
  - practice
  - intense training
  - labour
  - mining
- added dark mode and a switch between dark and light mode
- adjusted dashboard page so the policies card appear next to the time card even in mobile mode
- changed standings table:
  - points cell background is colored for podium finishes instead of font color
  - removed row coloring for closed seasons
  - centered points for competition finishes and point sums
- fixed standings page loading issue
- adjusted font sizes of card titles and header titles
- fixed policies not fetched during page load
- fixed console error about unique key prop in NewsContent

### 3.6 - Hall of Fame update

- refactored getting current grandmaster logic in backend to use new grandmasters table
  - this makes this logic more performant
- removed unused code for records
- added new 'Hall of Fame' page with three tabs:
  - Chronology: displays the list of champions in various leagues and list of grandmasters
  - Titles: displays the count of championships, wins, podiums etc.
  - Events: displays most wins by event type and record scores by league and event type
- made round titles on standings table centered

### 3.6.1

- changed blob icons on policy panel to material icons (their active colors remained the same)
- title of policies panel changed to "Policies"
- added contract and current standings information to blob details dialog
- added visualization for maintenance and administartion activities

### 3.7 - Traits and States update

- Added traits system
  - Each blob can have multiple traits that affect behavior and performance
  - Three trait types:
    - `HARD_WORKING`: increases preference for practice and labour activities
    - `DETERMINED`: reduces negative effects of `INJURED` and `TIRED` states
    - `LAZY`: increases preference for rest and free-time activities
  - Traits influence activity selection weights dynamically
  - Backend: new `traits` DB table, `TraitType` enum, `trait_repository`, and helper utilities

- Added states system
  - Each blob can have multiple active states with a duration (`effect_until` timestamp)
  - States affect training and event outcomes multiplicatively when multiple are active
  - Implemented state types and effects:
    - `INJURED`:
      - Training multiplier: ×0.2 (−80%)
      - Event multiplier: ×0.6 (−40%)
      - `DETERMINED` reduces training penalty (×0.5) and event penalty (×0.6→×0.6→ effectively handled in code as reduced chance/effect)
      - 15% chance during `PRACTICE` to refresh duration
    - `TIRED`:
      - Training multiplier: ×0.5 (−50%)
      - Event multiplier: ×0.8 (−20%)
      - `DETERMINED` reduces training penalty (to ×0.7/adjusted) and event penalty (further reduced)
      - 5% chance during `PRACTICE` and `LABOUR` to refresh duration
    - `GLOOMY`:
      - Training multiplier: ×0.85 (−15%)
      - Event multiplier: ×0.95 (−5%)
    - `FOCUSED`:
      - Training multiplier: ×1.2 (+20%)
      - In events: guarantees final strength/speed are at least 20% of the base stat (pre-modifiers)
    - `INTENSE_PRACTICE` (logical activity-state): used to model the side effects of intense practice; can create `TIRED` and `INJURED` states
  - Backend: new `states` DB table, `StateType` enum, `state_repository`, and helper utilities

- Activity and training behavior updates
  - New activity: `INTENSE_PRACTICE` — more efficient than regular practice (higher multiplier) but carries risk of `TIRED`/`INJURED`
  - Activity selection now uses weighted probabilities influenced by traits and active states

- Event scoring and DTOs
  - Event score generation now applies state-based multipliers at scoring time
  - `BlobCompetitorDto` now includes pre-loaded `states` to avoid repeated DB queries when scoring events
  - `FOCUSED` state provides a floor for event stats (20% of base) to keep focused blobs competitive

- Trait dynamics and randomization
  - On blob creation: 45% chance to receive an initial trait — either `HARD_WORKING` or `DETERMINED`; if one is assigned, 15% chance to also receive the other
  - Daily random states: if a blob has neither `GLOOMY` nor `FOCUSED`, it has a 1% chance to gain `GLOOMY` and a 1% chance to gain `FOCUSED` for the next day
  - High-integrity trait drift: if a blob's integrity > `INITIAL_INTEGRITY - CYCLES_PER_SEASON * 2`, it has a small chance to gain or lose a trait (configurable; currently implemented as a low-percent chance per day)
  - Trait conflict rules: `LAZY` will not be assigned to blobs that already have `HARD_WORKING` or `DETERMINED`, and vice-versa (prevents logically conflicting pairings)

- Bugfixes:
  - Hid standings label on blob details dialog when new season starts and there's no standings data available
  - Fixed new season news description
  - Fixed attendees on catchup training: dropout league members who already competed in dropout league last season are excluded
