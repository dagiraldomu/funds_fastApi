
# Funds BTG API (FastAPI)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Introduction
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## Features
- High-performance thanks to Starlette and Pydantic.
- Auto-generated interactive API documentation (Swagger UI and ReDoc).
- Dependency injection system.
- Asynchronous request handling.

## Installation

### Prerequisites
- Python 3.10+
- Git

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/dagiraldomu/fast-app.git
    cd fast-app
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Development Server
To start the development server, run:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
The API will be available at `http://127.0.0.1:8000`.

### Accessing API Documentation
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Deployment
### Using Docker
1. Build the Docker image:
    ```bash
    docker build -t app-image .
    ```

2. Run the Docker container:
    ```bash
    docker run -d --name app-container -p 8000:8000 app-image
    ```

### Deploying to a Cloud Provider
Refer to the specific cloud provider's documentation for deploying FastAPI applications (e.g., AWS, Azure, Google Cloud).

### aws configure


## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Open a Pull Request.

