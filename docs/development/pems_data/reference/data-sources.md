# Data sources

The data source components are responsible for the actual reading of data (the "how"). The design uses an abstract interface, `IDataSource`, to define a standard contract for any data source, making it easy to swap and compose implementations.

::: pems_data.sources.IDataSource

::: pems_data.sources.s3.S3DataSource

::: pems_data.sources.cache.CachingDataSource
