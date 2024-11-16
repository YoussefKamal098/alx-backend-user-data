# Simple API with Basic Authentication

A simple HTTP API to interact with the `User` model, including basic authentication.

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

### `api/v1/`

- **`app.py`**: Entry point for the API.
- **`views/index.py`**: Provides basic API endpoints such as `/status` and `/stats`.
- **`views/users.py`**: Contains all endpoints related to user management.
- **`auth/`**
  - **`auth.py`**: Authentication base class.
  - **`basic_auth.py`**: Implements Basic Authentication.

---

## Setup

1. Install the required dependencies:

   ```bash
   $ pip3 install -r requirements.txt
   ```

2. Set the environment variables:

   - `API_HOST` to define the host (e.g., `0.0.0.0`).
   - `API_PORT` to define the port (e.g., `5000`).
   - Optional: Set `AUTH_TYPE` to enable authentication (`"basic_auth"` for Basic Authentication).

---

## Run

Start the API with:

```bash
$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
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

---

## Authentication

### Overview

This API supports **Basic Authentication** to protect sensitive endpoints.

1. **Unauthorized Error Handler (`401`)**:  
   - If the `Authorization` header is missing, the API responds with:  
     ```json
     {"error": "Unauthorized"}
     ```

2. **Forbidden Error Handler (`403`)**:  
   - If the user is not authorized, the API responds with:  
     ```json
     {"error": "Forbidden"}
     ```

3. **Authentication Workflow**:
   - Extracts the `Authorization` header.
   - Decodes the Base64-encoded credentials.
   - Verifies the user's email and password against stored records.

---

## Example Usage

### Start the Server

```bash
$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
```

### Check API Status

```bash
$ curl http://0.0.0.0:5000/api/v1/status
{"status": "OK"}
```

### Authentication Example

#### Request with Valid Credentials

```bash
$ curl -u user@example.com:password123 http://0.0.0.0:5000/api/v1/users
```

#### Request without Credentials

```bash
$ curl http://0.0.0.0:5000/api/v1/users
{"error": "Unauthorized"}
```

#### Request with Invalid Credentials

```bash
$ curl -u user@example.com:wrongpassword http://0.0.0.0:5000/api/v1/users
{"error": "Forbidden"}
```

---

## Features Implemented

1. **Basic Endpoints**:
   - `/status` and `/stats` for API health monitoring.

2. **Error Handlers**:
   - Unauthorized (`401`) and Forbidden (`403`) handlers.

3. **User Management**:
   - Create, read, update, and delete users with authentication.

4. **Authentication Classes**:
   - `Auth`: Base class for authentication.
   - `BasicAuth`: Implements Basic Authentication.

5. **Secure Request Validation**:
   - Verifies requests using authorization headers.

---
