# Rates API

## Overview
The Rates API calculates average prices between routes for shipping freight. It provides endpoints to retrieve information about ports, regions, and prices.

## Schema
The database schema consists of the following entities:

- **Port**: Represents a port with attributes `code`, `name`, and `parent_slug`.
- **Region**: Represents a geographical region with attributes `slug`, `name`, and `parent_slug`.
- **Price**: Represents the price between source and destination ports on a specific date, with attributes `src_port_code`, `dest_port_code`, `date`, and `price`.

## API Endpoints
The API exposes the following endpoints:

- **/ports**: Retrieves information about ports. (Future work)
- **/regions**: Retrieves information about regions. (Future work)
- **/prices**: Retrieves average prices between routes for shipping freight. Users can specify source and destination ports, date range, and other filters.

## Usage
1. Clone the repository.
2. Run `docker-compose up --build`
3. Open SwaggerUI docs to play with API: `127.0.0.1:8000/docs`
4. Connect with local DB with the following credentials:
    ```
    POSTGRES_DB: xeneta_db
    POSTGRES_USER: xeneta_user
    POSTGRES_PASSWORD: xeneta_password
    POSTGRES_HOST: localhost
    POSTGRES_PORT: 5430
    ```

## Testing
The API includes unit tests to ensure the correctness of controllers, services, and repositories. Run the tests using a testing framework such as `pytest`.

## Dependencies
- Python 3.9
- PostgreSQL