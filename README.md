```
# calculator-backend
## Project Introduction
This is the Flask backend service for a separated web calculator. All mathematical calculations are executed on the server side. The system supports arithmetic operations, parentheses priority, decimal numbers and unary plus/minus. It handles exceptions including division by zero and invalid expressions, and uses SQLite to permanently store calculation history records.

## Tech Stack
Python3, Flask, SQLite3

## Operating Environment
Python 3.8 or above, supports Windows and Linux systems.

## Installation
1. Clone this repository
```bash
git clone https://github.com/YourUserName/calculator-backend.git
cd calculator-backend
```

2. Install required dependency packages

```
pip install flask
```

## Start Method

Run the following command to launch the backend service:

```
python app.py
```

The service listens on `0.0.0.0:5000` by default.

## Configuration

- Default service port: 5000. Modify the port parameter in app.py if you need to change it.
- For public network access, open TCP port 5000 in firewall or cloud server security group.

## Database Initialization

The SQLite database file `calculator.db` will be automatically created when the service runs for the first time. No manual SQL script execution is required.

## Connect with Frontend

This backend provides REST APIs for frontend interaction:

- POST `/calculate`: Receive mathematical expression and return calculation result or error message
- GET `/history`: Query all saved calculation history
- DELETE `/history`: Clear all calculation records
The frontend needs to configure its API address to match this backend service's IP and port.

## Other Notes

- Keep the terminal or cmd window open during service operation. Closing the window will stop the service.
- For 24-hour public access, deploy this project on cloud servers such as Tencent Cloud Light Application Server.
- Do not upload the generated `calculator.db` database file to GitHub.
