# Blob Championship System

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
