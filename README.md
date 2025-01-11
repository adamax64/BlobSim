# Blob Championship System
                        
<img src="./assets/blob.svg" alt="Blob Image" width="250"/>

This is a simulation software that simulates the life of fictional entities called the blobs and their competitions in a championships consists of multiple leagues throughout several seasons.

## Setup

### Prerequisites

The following requirements should be met to run the application on your device:

- Python 3.10 or newer

### Installation

1. Open a terminal in the root folder of the app

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up database an populate it with initial data:

    ```sh
    alembic upgrade head
    ```

## Running the application

To start the app, just run `start.bat`. This starts main.py using the local python interpreter of your device. 

For developing purposes there is a `debug.bat`, which runs the application in a smaller window and pauses the batch script if the python app crashes for some reason, so the user/developer can read the error message and stack before the window closes. 

If you use `debug.bat`, make sure to duplicate the database file and rename it to `bcs_database_debug.db`.

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
- Creation of a new blob

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
