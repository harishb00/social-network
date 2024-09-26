# Project
API for a social networking application using Django Rest Framework.

## Table of Contents
- [Installation](#installation)
- [Features](#features)
- [Examples](#examples)
- [API Documentation](#api-documentation)
- [Design Choices](#design-choices)
- [Next Steps](#next-steps)
- [References](#references)

## Installation

Ensure `Docker` is installed in your machine. You can download from [here](https://www.docker.com/products/docker-desktop/).

1. Clone the repository
```bash
git clone https://github.com/harishb00/social-network.git
cd social-network
```

2. Build Docker images as defined in the `docker-compose.yml` file and start the containers.
```bash
docker-compose up --build
```

### Poetry as Dependency Manager
* [Poetry](https://python-poetry.org/) is used as dependency manager for this project because of the several advantages it brings like
    - No need to manually maintain the `requirements.txt` file
    - Built-in dependency resolver
    - Automatically creates and manages virtual environment

## Features
* JWT based Authentication with refreshable tokens.
* Sign up with email.
* Login and Logout.
* Search users by name or email.
* Send friend requests to users.
* Accept/Reject friend requests.
* Block/Unblock an user.
* Rejected requests can be resent after a cool down period of 24 hours.
* List all the friends of logged in user.
* List all the pending friend requests sent to the user logged in (with sorting).
* Only authorized resources can be modified by logged in users.
* Pending requests and User search endpoints are paginated with 10 items per page.
* User rate throttling is used to limit the rate of friend requests sent in a minute.

## Examples
A Postman collection is exported and available as `Social API.postman_collection.json` in the repo. Download and import it to try out examples.

## API Documentation

### Authentication [`/api/v1/auth`]

- **Signup**
  - **URL:** `/signup/`
  - **Method:** `POST`
  - **Description:** Register a new user.
  - **Request:**
    ```json
    {
      "username": "newuser",
      "email": "newuser@email.com",
      "password": "password123",
      "password2": "password123",
      "name": "New User"
    }
    ```
  - **Response:**
    ```json
    {
        "id": 1,
        "username": "newuser",
        "email": "newuser@email.com",
        "name": "New User"
    }
    ```

- **Login**
  - **URL:** `/login/`
  - **Method:** `POST`
  - **Description:** Obtain a token pair (access and refresh tokens).
  - **Request:**
    ```json
    {
      "email": "user1",
      "password": "password123"
    }
    ```
  - **Response:**
    ```json
    {
      "access": "access_token",
      "refresh": "refresh_token"
    }
    ```

- **Refresh Token**
  - **URL:** `/login/refresh/`
  - **Method:** `POST`
  - **Description:** Refresh the access token.
  - **Request:**
    ```json
    {
      "refresh": "refresh_token"
    }
    ```
  - **Response:**
    ```json
    {
      "access": "new_access_token",
      "refresh": "new_refresh_token",
    }
    ```

- **Logout**
  - **URL:** `/logout/`
  - **Method:** `POST`
  - **Description:** Logout the user by invalidating the refresh token.
  - **Response:**
    ```json
    {
      "message": "Logged out successfully."
    }
    ```

### User Management [`/api/v1/users`]

- **List Users**
  - **URL:** `/`
  - **Method:** `GET`
  - **Description:** Retrieve a list of users (paginated).
  - **Response:**
    ```json
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 2,
                "username": "bharish",
                "email": "bharish@email.com",
                "name": "Harish B"
            },
            {
                "id": 3,
                "username": "jsurya",
                "email": "jsurya@email.com",
                "name": "Jaya Surya J"
            }
        ]
    }
    ```

- **Search Users**
  - **URL:** `/?search=keyword`
  - **Method:** `GET`
  - **Description:** Retrieve a list of users (paginated) by searching for the `keyword` that matches `email` or contains `username`.
  - **Response:**
    ```json
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 2,
                "username": "bharish",
                "email": "bharish@email.com",
                "name": "Harish B"
            },
            {
                "id": 3,
                "username": "jsurya",
                "email": "jsurya@email.com",
                "name": "Jaya Surya J"
            }
        ]
    }
    ```

### Friend Request Management [`api/v1/friend`]

- **List Friends**
  - **URL:** `/`
  - **Method:** `GET`
  - **Description:** Retrieve a list of friends.
  - **Response:**
    ```json
      [
          {
              "user_id": 2,
              "username": "bharish",
              "name": "Harish B"
          }
      ]
    ```

- **List Pending Requests**
  - **URL:** `/request/`
  - **Method:** `GET`
  - **Description:** Retrieve a list of pending friend requests.
  - **Response:**
    ```json
        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "id": 2,
                    "status": "pending",
                    "sender": "Bharath B",
                    "receiver": "Jaya Surya J"
                }
            ]
        }
    ```

- **List Pending Requests (Sort)**
  - **URL:** `/request/?ordering=-created_at`
  - **Method:** `GET`
  - **Description:** Retrieve a list of pending friend requests sorted by request time. Use `-` for descending order.
  - **Response:**
    ```json
        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "id": 2,
                    "status": "pending",
                    "sender": "Bharath B",
                    "receiver": "Jaya Surya J"
                }
            ]
        }
    ```

- **Send Friend Request**
  - **URL:** `/request/<int:pk>/`
  - **Method:** `POST`
  - **Description:** Send a friend request to a user.
  - **Parameters:**
    - `pk` (int): The ID of the user to send the request to.
  - **Response:**
    ```json
        {
            "id": 3,
            "status": "pending",
            "sender": "Bharath B",
            "receiver": "Jaya Surya J"
        }
    ```

- **Accept Friend Request**
  - **URL:** `/accept/<int:pk>/`
  - **Method:** `PUT`
  - **Description:** Accept a friend request.
  - **Parameters:**
    - `pk` (int): The ID of the friend request to accept.
  - **Response:**
    ```json
        {
            "id": 3,
            "status": "accepted",
            "sender": "Bharath B",
            "receiver": "Jaya Surya J"
        }
    ```

- **Reject Friend Request**
  - **URL:** `/reject/<int:pk>/`
  - **Method:** `PUT`
  - **Description:** Reject a friend request.
  - **Parameters:**
    - `pk` (int): The ID of the friend request to reject.
  - **Response:**
    ```json
    {
      "id": 1,
      "sender": "user1",
      "receiver": "user2",
      "status": "rejected"
    }
    ```


- **Block User**
  - **URL:** `/block/<int:user_id>/`
  - **Method:** `POST`
  - **Description:** Block a user.
  - **Parameters:**
    - `user_id` (int): The ID of the user to block.
  - **Response:**
    ```json
    {
      "message": "User blocked successfully."
    }
    ```

- **Unblock User**
  - **URL:** `/unblock/<int:user_id>/`
  - **Method:** `DELETE`
  - **Description:** Unblock a user.
  - **Parameters:**
    - `user_id` (int): The ID of the user to unblock.
  - **Response:**
    ```json
    {
      "message": "User unblocked successfully."
    }
    ```

## Design Choices
* Redis cache is used to cache response of getting friends list API endpoint. This is to ensure performance by returning cached results. The cache is invalidated when a new friend is added to account.
* Pagination is used for viewing pending friend requests and searching users to reduce the load and improve faster response times. This helps search requests which results in huge number of results.
* Throttling is used to limit number of friend requests a user can send in a minute. It's configured as **3 requests per minute**.

## Next Steps
* Add swagger documentation for APIs.
* Add unit tests.
* Ensure error response formats are consistent.

## References
* https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0
* https://dylancastillo.co/til/django-poetry-dockerfile.html
* https://medium.com/django-unleashed/securing-django-rest-apis-with-jwt-authentication-using-simple-jwt-a-step-by-step-guide-28efa84666fe