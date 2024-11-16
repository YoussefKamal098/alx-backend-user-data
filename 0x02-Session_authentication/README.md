# Simple API with Session Authentication

A simple HTTP API to interact with the `User` model, now enhanced with **Session Authentication** alongside the previously implemented **Basic Authentication**.

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

---

## Setup

1. Install the required dependencies:

   ```bash
   $ pip3 install -r requirements.txt
   ```

2. Set the environment variables:

    - `API_HOST`: Defines the host (e.g., `0.0.0.0`).
    - `API_PORT`: Defines the port (e.g., `5000`).
    - `AUTH_TYPE`: Selects the authentication method (`basic_auth`, `session_auth`, or `session_exp_auth`).
    - `SESSION_NAME`: Cookie name for storing the session ID (default: `_my_session_id`).
    - `SESSION_DURATION`: Duration (in seconds) for session validity (default: no expiration).

---

## Run

Start the API with:

```bash
$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_auth python3 -m api.v1.app
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

### Special User Route

- `GET /api/v1/users/me`: Retrieves the authenticated user object (using the session ID).

---

## Authentication

### Session Authentication Workflow

1. A session ID is generated for the user upon successful login and stored in the server.
2. The session ID is returned to the client as a cookie (`_my_session_id`).
3. Subsequent requests validate the session ID for authorization.

### Session Expiration

- When using `SessionExpAuth`, the session is valid only for a limited time:
    - Expiration is determined by `SESSION_DURATION`.
    - Expired sessions return `401 Unauthorized`.

---

## Example Usage

### Start the Server

```bash
$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_auth python3 -m api.v1.app
```

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

1. **Session vs. Basic Authentication**:
    - `basic_auth`: Authenticates every request with username and password.
    - `session_auth`: Uses cookies for persistent sessions, better for web applications.

2. **Session Expiration**:
    - Supported in `session_exp_auth`.
    - Ensures users are logged out after a certain duration of inactivity.

3. **Default Configuration**:
    - If `AUTH_TYPE` is not set, defaults to `basic_auth`.

---
