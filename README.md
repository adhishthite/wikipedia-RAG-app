# Flask App Template

This is a template of a Flask App that uses NGINX and GUNICORN for deployment.

## Overview

The Flask App Template is designed to provide a starting point for developing web applications using the Flask framework. It includes integration with NGINX and GUNICORN for efficient deployment.

## Features

- Integration with NGINX and GUNICORN
- Simplified structure for easy project initiation
- Use of best practices and recommended plugins
- Integration with Docker for easy deployment
- Use of MongoDB for data storage and Redis for caching
- Integrated with GitHub Actions

## Getting Started

To get started with this template, follow these steps:

0. Clone the repository.

    ```bash
    git clone https://github.com/adhishthite/flask-app-template
    ```

1. Navigate to the repository

    ```bash
    cd flask-app-template
    ```

2. Rename the `.env-t` file to `.env` and add/update the required environment variables.

    ```bash
    mv .env-t .env
    ```

3. Build the Docker image using docker-compose.

    ```bash
    docker-compose up --build
    ```


[WIP]


## License


## Feedback

I welcome feedback and suggestions. Please feel free to open an issue or submit a pull request.

---
