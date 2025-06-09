# Blob Championship System

<img src="./assets/blob.svg" alt="Blob Image" width="250"/>

This is a simulation software that simulates the life of fictional entities called the blobs and their competitions in a championships consists of multiple leagues throughout several seasons.

## Setup

### Prerequisites

The following requirements should be met to run the application on your device:

- Python 3.10 or newer
- Node 20.17.0 or newer
- npm 10.8.2 or newer

### Installation

#### Automatic instalation

Run `setup.bat` on Windows systems or `setup.sh` on Linux systems to setup the app .If you do not have permission to execute the script on Linux, open a terminal in the root folder of the project and give permission by running `chmod +x setup.sh` (you may need to add this permission to other scripts). This will create a virtual python environment where the backend will run, install the required python libraries. Then it will install the frontend dependencies and build the app for production as well. If you want to install the application manually, do the following steps below.

#### Backend

1. Open a terminal in the root folder of the app

2. Create a python virtual environment

   ```sh
   python -m venv .venv
   ```

3. Activate the environment

   - Windows:

   ```sh
   call venv\Scripts\activate
   ```

   -Linux

   ```sh
   source venv/bin/activate
   ```

4. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

5. Set up database an populate it with initial data:

   ```sh
   alembic upgrade head
   ```

#### Frontend

1. Go into folder `web-ui`

2. Run `npm install` to install node packages

3. If you want to run the app in production mode, run `npm run build` to build the production app

## Running the application

To start the app, just run `start.bat` on Windows systems or `start.sh` on Linux systems. This activates the virtual python environment, starts the backend, the frontend, and opens the frontend app on the system default browser. This opens three console windows, one for the frontend, one for the backend, and one for the main thread that started the application.

The application may need some time to load, so the opened browser tab may show that the page cannot be loaded. Wait for a few seconds in this case for the subsystem to start up properly.

The main thread waits for user input. When any key is pressed there (or enter on Linux), the script closes the frontend and backend server.

DISCLAIMER: closing the application result in killing ALL python and node processes!

For developing purposes there is a `debug.bat` (or `debug.sh` for Linux), which runs the application in development mode. If you use development mode, make sure to duplicate the database file and rename it to `bcs_database_debug.db`.

## Using the application

The simulation itself is completely self controlled. There is no way for the user to ruin the simulation, it can only ruin itself via a severe bug in the program :)

### Simulation time

Measuring time in the simulation is quite different from real life, so it is essential to understand how time works in BCS.

The smallest time unit of the simulation is called a cycle (can be considered as a day). Every step in the simulation progresses time by one cycle. The other time units are:

- Epoch (4 cycles)
- Season (32 epochs)
- Eon (4 Seasons)

Epochs divide the season into smaller parts like real life years consist of months. For the simulation it is essential to generate the season calendar (the dates for the championship events).

Seasons by meaning are the same as in real life sport championships.

In the application time is rendered in the following formats:

- Long format: Eon: `<eon>` Season: `<season>`. `<epoch>` - `<cycle>` (like `Eon: 2 Season: 9. 23 - 2`)
- Short format: `<season>`. `<epoch>` - `<cycle>` (like `5. 16 - 0`)

### Main workflow of the simulation

The user can progress the simulation by choosing the "_Proceed to next day_" option in the main menu.

This process can be blocked from time to time by the following cases:

- Championship event
- Creation of a new blob (only if there is no name suggestions the system can use to name new blobs)

If one of those cases are occuring, the user cannot proceed to the next day, they have to

- Simulate the championship event taking place of the current simulation cycle
- Create the new blob by giving it a name

Until the blockers are not done, the "Proceed to next day" option is not accessible and the simulation cannot move forward in time.

### Simulating the competitions

The user can start the simulation by choosing the "_Proceed to event_" option in the main menu if there is an unconcluded championship event.

On the event screen the user can progress the event step by step. Every step is an action from a blob, and is immediately saved to the database, so the user can quit the event simulation and go back to the event after some time and continue it where they left off.

At the end of the event the top three are highlighted by colors resemble bronze, silver and gold accordingly. If it was the last event of the season the final standings are also shown to the user before navigating back to the main menu.

### Other main menu options and views

- The "_View Blobs_" option navigate to a table that lists all currently living blobs and their carreer stats

- The "_View standings_" option navigates to a menu where the user can choose which league standings do they want to view

  - After choosing a league a table is shown with the standings of the current season. Here the user can navigate to other season standings by pressing the left and right arrow buttons

- The "_View Calendar_" option navigates to a screen that lists all of the championship events in the current season, where the next event is highlighted

## Changelog for newer versions

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
