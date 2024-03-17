# Wikipedia Crawler

This app crawls through Wikipedia and stores the pages in JSON files. The JSONs can be used for RAG and LLM-finetuning.
This is still a Work in Progress, so please feel expected to see some bugs.

## Overview

This Wikipedia Crawler has APIs to crawl through Wikipedia and store the pages in JSON files. The JSONs can be used for RAG and LLM-finetuning. The app is built using Flask and MongoDB for data storage. The app is containerized using Docker and can be deployed using GitHub Actions.

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
    git clone https://github.com/adhishthite/wikipedia-RAG-app.git
    ```

1. Navigate to the repository

    ```bash
    cd wikipedia-RAG-app
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
