# Introduction

The `pems_data` library provides a standardized, efficient interface for accessing Caltrans PeMS data within the project. It handles fetching data from the primary S3 data source and leverages a Redis-based caching layer to optimize performance for repeated requests.

This guide covers the specific setup and usage patterns for this library. For general development environment setup, please see the main [Getting started with development guide](../README.md).

## Prerequisites

Before using the library, ensure your environment is configured correctly.

### AWS credentials

The library's S3 data source requires AWS credentials to be available. The devcontainer is configured to use your host machine's AWS configuration. For details on setting this up via `aws configure sso`, please refer to the [Work with the Cloud infrastructure section in the main development guide](../README.md#work-with-the-cloud-infrastructure).

### Redis connection

A running Redis instance is required for the caching layer to function. The connection is configured with the following environment variables, which you can set in the `.env` file at the root of the project:

```env
# The hostname for the Redis server
REDIS_HOSTNAME=redis

# The port for the Redis server.
REDIS_PORT=6379
```

When running locally in the devcontainer, a `redis` service is started by Compose automatically.

## Architecture & Key concepts

The library is built around a few core components that work together to provide a simple data access experience.

- [`ServiceFactory`](./reference/service-factory.md): This is the primary entry point for using the library. It is a factory class that instantiates and wires together all the necessary dependencies, such as the data sources and caching clients.

- [**Services**](./reference/services.md): Services offer a high-level API for fetching specific, business-relevant data. For example, the `StationsService` has methods to get all station metadata for a given district or to retrieve 5-minute aggregated data for a specific station.

- [**Caching layer**](./reference/caching-layer.md): To minimize latency and load on the data source, the library uses a caching decorator by default. When a data request is made, this layer first checks the Redis cache for the requested data. If the data is not found (a cache miss), it retrieves the data from the underlying S3 source and stores it in the cache for future requests.

- [**Data sources**](./reference/data-sources.md): The underlying data source reads data directly from Parquet files stored in the Caltrans S3 bucket.

## Basic usage

Using the library involves creating the factory, getting a service, and calling a data-fetching method. The factory handles the underlying complexity of connecting to the data source and cache.

```python
from pems_data import ServiceFactory

# 1. Create the factory. This wires up all dependencies.
factory = ServiceFactory()

# 2. Request a pre-configured service.
stations_service = factory.stations_service()

# 3. Use the service to fetch data as a pandas DataFrame.
# This call will attempt to read from the cache first before
# falling back to the S3 data source.
district_7_metadata = stations_service.get_district_metadata(district_number="7")

print("Successfully fetched metadata for District 7:")
print(district_7_metadata.head())
```
