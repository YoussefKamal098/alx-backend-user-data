# User Authentication Service

This project implements a simple user authentication service in Python using Flask, SQLAlchemy, and bcrypt. It covers the basics of handling user registration, login, session management, and password reset.

## Requirements

- Python 3.7
- SQLAlchemy 1.3.x
- pycodestyle 2.5
- bcrypt

To install the required dependencies, you can run:

```bash
pip install -r requirements.txt
```

## Project Structure

- **`user.py`**: Contains the SQLAlchemy `User` model.
- **`db.py`**: Contains the `DB` class to interact with the database.
- **`auth.py`**: Contains authentication-related methods like hashing passwords and managing sessions.
- **`app.py`**: Flask application that exposes the user authentication API.
- **`main.py`**: End-to-end integration tests for the authentication system.

## Features and Tasks Completed

### 1. **User Model**
- Created a `User` model with attributes like `id`, `email`, `hashed_password`, `session_id`, and `reset_token`.

### 2. **Database Operations**
- Implemented methods for adding, updating, and finding users in the database:
    - `add_user`: Adds a new user to the database.
    - `delete_user`: Deletes user from the database.
    - `find_user_by`: Finds a user based on specified criteria.
    - `update_user`: Updates user attributes.

### 3. **Password Hashing and User Registration**
- Implemented password hashing with bcrypt and user registration in the `Auth` class.
- When registering a new user, it checks for existing users by email and raises appropriate errors if the user already exists.

### 4. **Session Management**
- Added functionality for creating, retrieving, and destroying user sessions using UUIDs.
- Users can log in and receive a session ID, which is stored in a cookie.

### 5. **Password Reset**
- Implemented password reset functionality:
    - `get_reset_password_token`: Generates a reset token for password recovery.
    - `update_password`: Allows users to reset their password using the reset token.

### 6. **Flask API Endpoints**
- Implemented the following Flask routes:
    - **`POST /users`**: Register a new user.
    - **`DELETE /users/<email>`**: Unregister the existing user
    - **`POST /sessions`**: User login.
    - **`GET /profile`**: Retrieve the profile of a logged-in user.
    - **`DELETE /sessions`**: Log out a user.
    - **`POST /reset_password`**: Request a password reset token.
    - **`PUT /reset_password`**: Reset a user's password.

### 7. **Integration Tests**
- Created end-to-end tests for the authentication service using the `requests` module.
- The tests cover user registration, login, profile access, password reset, and session management.

## How to Use

1. **Run the Flask Application**:
   Start the Flask application by running the following command:

   ```bash
   python3 app.py
   ```

2. **Test Authentication with cURL or Postman**:
   You can test the authentication service by sending HTTP requests to the API endpoints:

    - **Register User** (POST /users):
      ```bash
      curl -X POST -F "email=user@example.com" -F "password=secret" http://127.0.0.1:5000/users
      ```
    - **Unregister User** (DELETE /users/<email>):
       ```bash
       curl -X DELETE http://127.0.0.1:5000/users/<email>
       ```

    - **Login** (POST /sessions):
      ```bash
      curl -X POST -F "email=user@example.com" -F "password=secret" http://127.0.0.1:5000/sessions
      ```

    - **View Profile** (GET /profile):
      ```bash
      curl -X GET --cookie "session_id=<SESSION_ID>" http://127.0.0.1:5000/profile
      ```

    - **Password Reset** (POST /reset_password):
      ```bash
      curl -X POST -F "email=user@example.com" http://127.0.0.1:5000/reset_password
      ```

    - **Update Password** (PUT /reset_password):
      ```bash
      curl -X PUT -F "email=user@example.com" -F "reset_token=<TOKEN>" -F "new_password=newsecret" http://127.0.0.1:5000/reset_password
      ```

3. **Run Integration Tests**:
   To run the integration tests, execute the following:

   ```bash
   python3 main.py
   ```

   If everything is correct, the tests will pass with no output.
