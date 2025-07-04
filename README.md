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

## Version changelog

[Changelog for newer versions](./CHANGELOG.md)
