# Simple API with Session Authentication and Session Persistence

A simple HTTP API to interact with the `User` model, now enhanced with **Session Authentication** and **Session Persistence** using a database. This ensures sessions persist even after server restarts, providing a more robust and scalable authentication mechanism.

---

## Requirements

### Python Scripts

1. **Compatibility**:
    - All scripts are interpreted/compiled on **Ubuntu 18.04 LTS** using Python 3.7.

2. **File Standards**:
    - Every file must end with a **new line**.
    - The first line of each file must be:
      ```python
      #!/usr/bin/env python3
      ```

3. **Documentation**:
    - A `README.md` file at the project root is mandatory.
    - All modules, classes, and functions must include clear and meaningful documentation:
        - **Module**: `python3 -c 'print(__import__("my_module").__doc__)'`
        - **Class**: `python3 -c 'print(__import__("my_module").MyClass.__doc__)'`
        - **Function**:
          ```bash
          python3 -c 'print(__import__("my_module").my_function.__doc__)'
          python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'
          ```
    - Documentation must be descriptive and include a complete sentence explaining the purpose of the module, class, or function.

4. **Code Style**:
    - Follow **pycodestyle** standards (version 2.5).

5. **Executability**:
    - All files must be executable.

6. **File Length**:
    - The length of files will be tested using the `wc` command.

---

## Files

### `models/`

- **`base.py`**: Base model for API objects, handles serialization to file.
- **`user.py`**: `User` model implementation.
- **`user_session.py`**: Implements the `UserSession` model for managing session persistence using a database.

### `api/v1/`

- **`app.py`**: Entry point for the API, dynamically initializes the appropriate authentication system based on the `AUTH_TYPE` environment variable.
- **`views/`**
    - **`index.py`**: Provides basic API endpoints such as `/status` and `/stats`.
    - **`users.py`**: Contains all endpoints related to user management.
    - **`session_auth.py`**: Contains endpoints for session authentication management.
- **`auth/`**
    - **`auth.py`**: Authentication base class with utilities for managing authorization headers and session cookies.
    - **`basic_auth.py`**: Implements Basic Authentication.
    - **`session_auth.py`**: Implements session-based authentication, including creation and validation of sessions.
    - **`session_exp_auth.py`**: Extends `SessionAuth` by adding session expiration logic.
    - **`session_db_auth.py`**: Implements session authentication with session persistence using the `UserSession` model.
    - **`auth_factory.py`**: Abstract factory module for creating different authentication instances (`BasicAuth`, `SessionAuth`, and `SessionExpAuth`).
    - **`auth_factory_provider.py`**: Manages authentication factories dynamically, allowing for the addition and removal of custom authentication mechanisms.

### Root Directory

- **`utils.py`**: **Utility module** that includes helper functions and decorators such as `@override` to enforce subclass method overriding.

---

## Features Implemented

### 1. **Basic Authentication**
- Authenticate users via Basic Authentication headers.
- Endpoints supported:
    - `GET /api/v1/users`
    - `POST /api/v1/users`
    - `GET /api/v1/users/<user_id>`
    - `PUT /api/v1/users/<user_id>`
    - `DELETE /api/v1/users/<user_id>`

### 2. **Session Authentication**
- Authenticate users via Session IDs stored in cookies.
- Includes support for session expiration.

### 3. **Session Persistence (New Feature)**
- **What is it?**: Sessions are now stored in a database using the `UserSession` model. This ensures that sessions persist even after server restarts.
- **Implemented in**: `SessionDBAuth` class.
- **Advantages**:
    - Sessions are no longer lost when the server restarts.
    - Allows for scaling and better session management.
- **Environment Variable**: `AUTH_TYPE=session_db_auth`.

---

## Setup

1. Install the required dependencies:

   ```bash
   $ pip3 install -r requirements.txt
   ```

2. Set the environment variables:

    - `API_HOST`: Defines the host (e.g., `0.0.0.0`).
    - `API_PORT`: Defines the port (e.g., `5000`).
    - `AUTH_TYPE`: Selects the authentication method (`basic_auth`, `session_auth`, `session_exp_auth`, or `session_db_auth`).
    - `SESSION_NAME`: Cookie name for storing the session ID (default: `_my_session_id`).
    - `SESSION_DURATION`: Duration (in seconds) for session validity (default: no expiration).

---

## Run

Start the API with:

```bash
$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_db_auth SESSION_NAME=_my_session_id SESSION_DURATION=60 python3 -m api.v1.app
```

---

## Routes

### General Endpoints

- `GET /api/v1/status`: Returns the status of the API.
- `GET /api/v1/stats`: Provides statistics about the API.

### User Management

- `GET /api/v1/users`: Retrieves a list of all users.
- `GET /api/v1/users/<id>`: Retrieves a specific user by their ID.
- `POST /api/v1/users`: Creates a new user. Requires JSON payload:
    - `email` (required)
    - `password` (required)
    - `last_name` (optional)
    - `first_name` (optional)
- `PUT /api/v1/users/<id>`: Updates an existing user by their ID. Requires JSON payload:
    - `last_name` (optional)
    - `first_name` (optional)
- `DELETE /api/v1/users/<id>`: Deletes a specific user by their ID.

### Session Management

- `POST /api/v1/auth_session/login`: Authenticates a user via email and password, creating a session.
- `DELETE /api/v1/auth_session/logout`: Logs out the user by destroying their session.

---

## Example Usage

### Authenticate a User

#### Login

```bash
$ curl -X POST -d "email=user@example.com" -d "password=password123" http://0.0.0.0:5000/api/v1/auth_session/login
```

#### Access Resources

```bash
$ curl -X GET --cookie "_my_session_id=<SESSION_ID>" http://0.0.0.0:5000/api/v1/users/me
```

#### Logout

```bash
$ curl -X DELETE --cookie "_my_session_id=<SESSION_ID>" http://0.0.0.0:5000/api/v1/auth_session/logout
```

---

## Notes

1. **Session Persistence**:
    - Sessions stored in the `UserSession` database are persisted across server restarts.
    - Configurable via `AUTH_TYPE=session_db_auth`.

2. **Session Expiration**:
    - Supported in `SessionExpAuth` and `SessionDBAuth`.
    - Expired sessions are automatically invalidated based on `SESSION_DURATION`.

3. **Default Configuration**:
    - If `AUTH_TYPE` is not set, defaults to `basic_auth`.
