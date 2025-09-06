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
