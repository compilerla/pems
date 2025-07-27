"""Helpers for serializing specific data types e.g. for storing/retrieving from a cache."""

import pandas as pd
import pyarrow as pa
import pyarrow.ipc as ipc


def arrow_bytes_to_df(arrow_buffer: bytes) -> pd.DataFrame:
    """Deserializes Arrow IPC format bytes back to a DataFrame.

    Args:
        arrow_buffer (bytes): A buffer of Arrow IPC bytes representing a DataFrame

    Returns:
        value (pandas.DataFrame): The DataFrame deserialized from the buffer, or an empty DataFrame if the buffer was empty.
    """
    if not arrow_buffer:
        return pd.DataFrame()
    # deserialize the Arrow IPC stream
    with pa.BufferReader(arrow_buffer) as buffer:
        # the reader reconstructs the Arrow Table from the buffer
        reader = ipc.RecordBatchStreamReader(buffer)
        arrow_table = reader.read_all()
    return arrow_table.to_pandas()


def df_to_arrow_bytes(df: pd.DataFrame) -> bytes:
    """Serializes a DataFrame to Arrow IPC format bytes.

    Args:
        df (pandas.DataFrame): The DataFrame to serialize

    Returns:
        value (bytes): The Arrow IPC format bytes representation of the DataFrame.
    """
    if df.empty:
        return b""
    # convert DataFrame to an Arrow Table
    arrow_table = pa.Table.from_pandas(df, preserve_index=False)
    # serialize the Arrow Table to bytes using the IPC stream format
    sink = pa.BufferOutputStream()
    with ipc.RecordBatchStreamWriter(sink, arrow_table.schema) as writer:
        writer.write_table(arrow_table)
    # get the buffer from the stream
    return sink.getvalue().to_pybytes()
