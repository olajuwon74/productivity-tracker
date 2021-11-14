# PRODUCTIVITY TRACKER

## Dependencies

- [Python3 (the programming language)](https://www.python.org)
- [Flask (the web framework)](https://flask.palletsprojects.com)

## To Run

### Initialize Project

- create virtual environment at the project's root. The virtual environment is used to isolate libraries and dependencies across various project on the local system

  `python3 venv -m venv`

- activate virtual environment.

  - For windows: `venv\bin\activate.bat`
  - For Linux/Mac: `source venv/bin/activate`

- update pip and install requirements.

  - `pip install --upgrade pip`
  - `pip install -r requirements.txt`

- deactivate virtual environment

  - `deactivate`

PS: You only need to initialize the project once

### Run the Project

- Activate virtual environment

  - For windows: `venv\bin\activate.bat`
  - For Linux/Mac: `source venv/bin/activate`

- Run server
  - `flask run`

Application can be accessed at [http://localhost:5000](http://localhost:5000)

- (Optional) To change the default port from 5000 to 8080 or any other port, run
  - For windows: `set FLASK_RUN_PORT=8080`
  - For Linux/Mac: `export FLASK_RUN_PORT=8080`

    before running the server.
