# Project Dogs API

## Requirements

- Python 3.7+
- autopep8
- requests
- pymongo
- fastapi
- uvicorn

## Installation

Clone the repository and install the requirements.

```bash
git clone https://github.com/zoenr/api-dogs.git
cd api-dogs
pip install -r requirements.txt
```

## Usage

Start the development server with FastAPI or Uvicorn.

```bash
# FastAPI
fastapi dev main.py --reload
```

```bash
# Uvicorn
uvicorn main:app --reload
```

## Endpoints

### GET /api/dogs

Returns a list of all dogs.

### GET /api/dogs/is_adopted

Returns a list of all dogs that are adopted.

### GET /api/dogs/{name}

Returns a specific dog.

### POST /api/dogs/{name}

Creates a new dog.

### PUT /api/dogs/{name}

Updates a specific dog.

### DELETE /api/dogs/{name}

Deletes a specific dog.

## Middleware

The `middleware` folder contains middlewares used in the project.

### rate_limit

This middleware limits the number of requests per minute.
