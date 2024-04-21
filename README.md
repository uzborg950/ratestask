# Rates API

## Overview

The Rates API calculates average prices between routes for shipping freight. It provides endpoints to retrieve
information about ports, regions, and prices.

## Schema

The database schema consists of the following entities:

- **Port**: Represents a port with attributes `code`, `name`, and `parent_slug`.
- **Region**: Represents a geographical region with attributes `slug`, `name`, and `parent_slug`.
- **Price**: Represents the price between source and destination ports on a specific date, with
  attributes `src_port_code`, `dest_port_code`, `date`, and `price`.

## API Endpoints

The API exposes the following endpoints:

- **/ports**: Retrieves information about ports. (Future work)
- **/regions**: Retrieves information about regions. (Future work)
- **/prices**: Retrieves average prices between routes for shipping freight. Users can specify source and destination
  ports, date range, and other filters.

## Usage

1. Clone the repository.
2. Run `docker-compose up --build`
3. Open SwaggerUI docs to play with API: `localhost:8000/docs`


## Testing

This repository includes unit tests for services and integration tests for DB repository layers. This is not an exhaustive test
coverage, but it covers the most complex parts of the API. I would always recommend complete test coverage though.

    1. unit test files are suffixed with _unit
    2. integration test files are suffixed with _int

To run:
1. ```pip install -r requirements_dev.txt``` 
2. ```Run the tests using pytest```

## Dependencies
- python 3.9
- fastapi
- pydantic
- uvicorn
- psycopg2-binary
- postgres:latest